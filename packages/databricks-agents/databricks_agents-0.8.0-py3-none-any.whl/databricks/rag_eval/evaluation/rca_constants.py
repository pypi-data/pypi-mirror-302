# Root cause analysis snippets
from databricks.rag_eval.config import assessment_config

CHUNK_PRECISION_IS_LOW_MESSAGE = (
    "The root cause of failure is traced to the negative ratings of "
    f"{assessment_config.CHUNK_RELEVANCE.assessment_name} which marked all retrieved "
    "chunks as irrelevant to the question. "
    f"See the {assessment_config.CHUNK_RELEVANCE.assessment_name} rationale for more details."
)

PER_CHUNK_ASSESSMENTS_FAIL_MESSAGE = (
    "The root cause of failure is traced to the negative per-chunk ratings of {judge_name}. "
    "See the {judge_name} rationale for more details."
)

DEFAULT_FAIL_MESSAGE = (
    "The root cause of failure is traced to the negative rating of {judge_name}. "
    "See the {judge_name} rationale for more details."
)

SUGGESTED_ACTIONS = {
    assessment_config.CONTEXT_SUFFICIENCY.assessment_name: (
        "First, you should ensure that the vector DB contains the "
        "missing information. Second, you should tune your retrieval "
        "step to retrieve the missing information (see the judges' rationales to understand what's missing). "
        "Here are some methods that you can try for this: retrieving more chunks, trying different embedding models, "
        "or over-fetching & reranking results."
    ),
    assessment_config.CHUNK_RELEVANCE.assessment_name: (
        "First, you should ensure that relevant chunks are present in the "
        "vector DB. Second, you should tune your retrieval step to retrieve the missing information (see the judges' "
        "rationales to understand what's missing). Here are some methods that you can try for this: "
        "retrieving more chunks, trying different embedding models, or over-fetching & reranking results."
    ),
    assessment_config.HARMFULNESS.assessment_name: (
        "Consider implementing guardrails to prevent harmful content or a "
        "post-processing step to filter out harmful content."
    ),
    assessment_config.RELEVANCE_TO_QUERY.assessment_name: (
        "Consider improving the prompt template to encourage direct, "
        "specific responses, re-ranking retrievals to provide more relevant chunks to the LLM earlier "
        "in the prompt, or using a more capable LLM."
    ),
    assessment_config.GROUNDEDNESS.assessment_name: (
        "Consider updating the prompt template to emphasize "
        "reliance on retrieved context, using a more capable LLM, or implementing a post-generation "
        "verification step."
    ),
    assessment_config.CORRECTNESS.assessment_name: (
        "Consider improving the prompt template to encourage direct, "
        "specific responses, re-ranking retrievals to provide more relevant chunks to the LLM earlier in "
        "the prompt, or using a more capable LLM."
    ),
}
