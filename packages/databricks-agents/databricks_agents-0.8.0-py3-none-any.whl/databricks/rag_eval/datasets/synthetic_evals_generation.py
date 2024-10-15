import hashlib
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Union

import pandas as pd
from tqdm.auto import tqdm

from databricks.rag_eval import context, env_vars
from databricks.rag_eval.datasets import entities as datasets_entities
from databricks.rag_eval.evaluation import entities as eval_entities
from databricks.rag_eval.utils import error_utils, rate_limit

_logger = logging.getLogger(__name__)


_ANSWER_TYPES = [datasets_entities.SyntheticAnswerType.MINIMAL_FACTS]


@context.eval_context
def generate_evals_df(
    docs: Union[pd.DataFrame, "pyspark.sql.DataFrame"],  # noqa: F821
    *,
    num_evals_per_doc: int = 1,
    example_questions: Optional[Union[List[str], pd.DataFrame, pd.Series]] = None,
) -> pd.DataFrame:
    """
    Run the synthetic generation pipeline to generate evaluations for a given set of documents.
    Generated evaluation set can be used with Databricks Agent Evaluation (https://docs.databricks.com/en/generative-ai/agent-evaluation/evaluate-agent.html).

    :param docs: A pandas/Spark DataFrame with a text column `content` and a `doc_uri` column.
    :param num_evals_per_doc: The number of evaluations to generate for each document. Default is 1.
    :param example_questions: Optional list of example questions to guide the synthetic generation.
        It can be a list of strings, a pandas Series of strings, or a pandas DataFrame with a single string column.
        Evaluation questions will be generated in a style that is similar to the questions you provide, which can come
        from existing evals, production logs, or queries you provide directly.
    """
    # Configs
    max_num_evals_per_doc = (
        env_vars.AGENT_EVAL_GENERATE_EVALS_MAX_NUM_EVALS_PER_DOC.get()
    )
    max_num_example_question = (
        env_vars.AGENT_EVAL_GENERATE_EVALS_MAX_NUM_EXAMPLE_QUESTIONS.get()
    )
    question_generation_rate_limit_config = rate_limit.RateLimitConfig(
        quota=env_vars.AGENT_EVAL_GENERATE_EVALS_QUESTION_GENERATION_RATE_LIMIT_QUOTA.get(),
        time_window_in_seconds=env_vars.AGENT_EVAL_GENERATE_EVALS_QUESTION_GENERATION_RATE_LIMIT_TIME_WINDOW_IN_SECONDS.get(),
    )
    answer_generation_rate_limit_config = rate_limit.RateLimitConfig(
        quota=env_vars.AGENT_EVAL_GENERATE_EVALS_ANSWER_GENERATION_RATE_LIMIT_QUOTA.get(),
        time_window_in_seconds=env_vars.AGENT_EVAL_GENERATE_EVALS_ANSWER_GENERATION_RATE_LIMIT_TIME_WINDOW_IN_SECONDS.get(),
    )
    max_workers = env_vars.RAG_EVAL_MAX_WORKERS.get()

    # Input validation
    if not isinstance(num_evals_per_doc, int):
        raise error_utils.ValidationError(
            "num_evals_per_doc must be a positive integer."
        )
    if num_evals_per_doc < 1:
        raise error_utils.ValidationError("num_evals_per_doc must be at least 1.")
    if num_evals_per_doc > max_num_evals_per_doc:
        raise error_utils.ValidationError(
            f"num_evals_per_doc exceeds the limit of {max_num_evals_per_doc}."
        )
    example_questions = _read_example_questions(example_questions)
    if example_questions and len(example_questions) > max_num_example_question:
        example_questions = example_questions[:max_num_example_question]
        _logger.warning(
            f"example_questions has been truncated to {max_num_example_question} items."
        )

    # Rate limiters
    question_generation_rate_limiter = rate_limit.RateLimiter.build_from_config(
        question_generation_rate_limit_config
    )
    answer_generation_rate_limiter = rate_limit.RateLimiter.build_from_config(
        answer_generation_rate_limit_config
    )

    generate_evals: List[eval_entities.EvalItem] = []
    docs: List[datasets_entities.Document] = _read_docs(docs)

    with ThreadPoolExecutor(max_workers) as executor:
        futures = [
            executor.submit(
                _generate_evals_for_doc,
                doc=doc,
                num_evals=num_evals_per_doc,
                example_questions=example_questions,
                question_generation_rate_limiter=question_generation_rate_limiter,
                answer_generation_rate_limiter=answer_generation_rate_limiter,
            )
            for doc in docs
        ]

        futures_as_completed = as_completed(futures)
        # Add a progress bar to show the progress of the assessments
        futures_as_completed = tqdm(
            futures_as_completed,
            total=len(futures),
            disable=False,
            desc="Generating evaluations",
            smoothing=0,  # 0 means using average speed for remaining time estimates
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} documents processed [Elapsed: {elapsed}, Remaining: {remaining}]",
        )

        try:
            for future in futures_as_completed:
                result = future.result()
                generate_evals.extend(result)
        except KeyboardInterrupt:
            for future in futures:
                future.cancel()
            _logger.info("Generation interrupted.")
            raise

    return pd.DataFrame(
        [pd.Series(generate_eval.as_dict()) for generate_eval in generate_evals]
    )


def _generate_evals_for_doc(
    doc: datasets_entities.Document,
    num_evals: int,
    example_questions: Optional[List[str]],
    question_generation_rate_limiter: rate_limit.RateLimiter,
    answer_generation_rate_limiter: rate_limit.RateLimiter,
) -> List[eval_entities.EvalItem]:
    """
    Generate evaluations for a single document.

    :param doc: the document to generate evaluations for
    :param num_evals: the number of evaluations to generate
    :param example_questions: optional list of example questions to guide the synthetic generation
    :param question_generation_rate_limiter: rate limiter for question generation
    :param answer_generation_rate_limiter: rate limiter for answer generation
    """
    if not doc.content or not doc.content.strip():
        _logger.warning(f"Skip {doc.doc_uri} because it has empty content.")
        return []
    max_doc_content_chars = (
        env_vars.AGENT_EVAL_GENERATE_EVALS_MAX_DOC_CONTENT_CHARS.get()
    )
    if len(doc.content) > max_doc_content_chars:
        doc.content = doc.content[:max_doc_content_chars]
        _logger.warning(
            f"Truncated the content of {doc.doc_uri} to {max_doc_content_chars} characters."
        )

    client = _get_managed_evals_client()
    with question_generation_rate_limiter:
        try:
            generated_questions = client.generate_questions(
                doc=doc, num_questions=num_evals, example_questions=example_questions
            )
        except Exception as e:
            _logger.warning(f"Failed to generate questions for doc {doc.doc_uri}: {e}")
            return []

    if not generated_questions:
        return []

    generated_answers: List[datasets_entities.SyntheticAnswer] = []
    # Use a thread pool to run answer generation in parallel
    # Use the number of questions as the number of workers
    with ThreadPoolExecutor(max_workers=len(generated_questions)) as executor:
        futures = [
            executor.submit(
                _generate_answer_for_question,
                question=question,
                answer_generation_rate_limiter=answer_generation_rate_limiter,
            )
            for question in generated_questions
        ]

        try:
            for future in as_completed(futures):
                result = future.result()
                generated_answers.append(result)
        except KeyboardInterrupt:
            for future in futures:
                future.cancel()
            _logger.info("Generation interrupted.")
            raise
    return [
        eval_entities.EvalItem(
            question_id=hashlib.sha256(
                generated_answer.question.question.encode()
            ).hexdigest(),
            question=generated_answer.question.question,
            ground_truth_answer=generated_answer.synthetic_ground_truth,
            ground_truth_retrieval_context=eval_entities.RetrievalContext(
                chunks=[
                    eval_entities.Chunk(
                        doc_uri=generated_answer.question.source_doc_uri,
                        content=generated_answer.question.source_context,
                    )
                ]
            ),
            grading_notes=generated_answer.synthetic_grading_notes,
            expected_facts=generated_answer.synthetic_minimal_facts,
        )
        for generated_answer in generated_answers
        if generated_answer is not None
    ]


def _generate_answer_for_question(
    question: datasets_entities.SyntheticQuestion,
    answer_generation_rate_limiter: rate_limit.RateLimiter,
) -> Optional[datasets_entities.SyntheticAnswer]:
    """
    Generate an answer for a single question.

    :param question: the question to generate an answer for
    :param answer_generation_rate_limiter: rate limiter for answer generation
    """
    if not question.question or not question.question.strip():
        # Skip empty questions
        return None

    client = _get_managed_evals_client()
    with answer_generation_rate_limiter:
        try:
            return client.generate_answer(question=question, answer_types=_ANSWER_TYPES)
        except Exception as e:
            _logger.warning(
                f"Failed to generate answer for question '{question.question}': {e}"
            )
            return None


def _read_example_questions(
    example_questions: Optional[Union[List[str], pd.DataFrame, pd.Series]],
) -> Optional[List[str]]:
    """
    Read example questions from the input.
    """
    if example_questions is None:
        return None

    if isinstance(example_questions, pd.DataFrame):
        if not len(example_questions.columns) == 1:
            raise error_utils.ValidationError(
                "example_questions DataFrame must have a single string column"
            )
        return example_questions.iloc[:, 0].to_list()

    if isinstance(example_questions, pd.Series):
        return example_questions.to_list()

    if isinstance(example_questions, List):
        return list(example_questions)

    raise error_utils.ValidationError(
        f"Unsupported type for example_questions: {type(example_questions)}."
        "It can be a list of strings, a pandas Series of strings, or a pandas DataFrame with a single string column."
    )


def _read_docs(
    docs: Union[pd.DataFrame, "pyspark.sql.DataFrame"],  # noqa: F821
) -> List[datasets_entities.Document]:
    """
    Read documents from the input pandas/Spark DateFrame.
    """
    if docs is None:
        raise error_utils.ValidationError("Input docs must not be None.")

    if isinstance(docs, pd.DataFrame):
        # read from pandas DataFrame
        return _read_docs_from_pandas_df(docs)

    # Import pyspark here to avoid hard dependency on pyspark
    import pyspark.sql.connect.dataframe

    if isinstance(
        docs, (pyspark.sql.DataFrame, pyspark.sql.connect.dataframe.DataFrame)
    ):
        # read from Spark DataFrame
        return _read_docs_from_spark_df(docs)

    raise ValueError(
        f"Unsupported type for docs: {type(docs)}. "
        f"It can be a pandas/Spark DataFrame with a text column `content` and a `doc_uri` column."
    )


def _read_docs_from_pandas_df(pd_df: pd.DataFrame) -> List[datasets_entities.Document]:
    """
    Read documents from a pandas DataFrame.
    """
    # check if the input DataFrame has the required columns
    if "doc_uri" not in pd_df.columns or "content" not in pd_df.columns:
        raise error_utils.ValidationError(
            "Input docs DataFrame must have 'doc_uri' and 'content' columns."
        )
    return [
        datasets_entities.Document(
            doc_uri=row["doc_uri"],
            content=row["content"],
        )
        for _, row in pd_df.iterrows()
    ]


def _read_docs_from_spark_df(
    spark_df: "pyspark.sql.DataFrame",  # noqa: F821
) -> List[datasets_entities.Document]:
    """
    Read documents from a Spark DataFrame.
    """
    # check if the input DataFrame has the required columns
    if "doc_uri" not in spark_df.columns or "content" not in spark_df.columns:
        raise error_utils.ValidationError(
            "Input DataFrame must have 'doc_uri' and 'content' columns"
        )
    return [
        datasets_entities.Document(
            doc_uri=row.asDict()["doc_uri"],
            content=row.asDict()["content"],
        )
        for row in spark_df.collect()
    ]


def _get_managed_evals_client():
    """
    Get a managed evals client.
    """
    return context.get_context().build_managed_evals_client()
