from typing import Collection, Dict, List, Optional

import requests
from urllib3.util import retry

from databricks.rag_eval import env_vars
from databricks.rag_eval.clients import databricks_api_client
from databricks.rag_eval.datasets import entities

_DEFAULT_RETRY_CONFIG_FOR_SYNTHETIC_GENERATION = retry.Retry(
    total=env_vars.AGENT_EVAL_GENERATE_EVALS_MAX_RETRIES.get(),
    backoff_factor=env_vars.AGENT_EVAL_GENERATE_EVALS_BACKOFF_FACTOR.get(),
    status_forcelist=[429, 500, 502, 503, 504],
    backoff_jitter=env_vars.AGENT_EVAL_GENERATE_EVALS_BACKOFF_JITTER.get(),
    allowed_methods=frozenset(["GET", "POST"]),  # by default, it doesn't retry on POST
)


def _raise_for_status(resp: requests.Response) -> None:
    """
    Raise an Exception if the response is an error.
    Custom error message is extracted from the response JSON.
    """
    if resp.status_code == requests.codes.ok:
        return
    http_error_msg = ""
    if 400 <= resp.status_code < 500:
        http_error_msg = f"{resp.status_code} Client Error: {resp.reason}. "
    elif 500 <= resp.status_code < 600:
        http_error_msg = f"{resp.status_code} Server Error: {resp.reason}. "
    resp_json = resp.json() or {}
    error_msg = resp_json.get("message", "")
    raise requests.HTTPError(http_error_msg + error_msg, response=resp)


class ManagedEvalsClient(databricks_api_client.DatabricksAPIClient):
    """
    Client to interact with the managed-evals service.
    """

    def __init__(
        self,
        api_url: str,
        api_token: str,
    ):
        super().__init__(
            api_url=api_url,
            api_token=api_token,
            version="2.0",
        )

    def _request_post(
        self,
        url: str,
        json: Dict[str, str],
        retry_config: Optional[
            retry.Retry
        ] = _DEFAULT_RETRY_CONFIG_FOR_SYNTHETIC_GENERATION,
    ):
        with self.get_request_session(retry_config) as request_session:
            return request_session.post(
                self.get_method_url(url),
                json=json,
                auth=self.get_auth(),
            )

    def generate_questions(
        self,
        *,
        doc: entities.Document,
        num_questions: int,
        example_questions: List[str],
    ) -> List[entities.SyntheticQuestion]:
        """
        Generate synthetic questions for the given document.
        """
        request_json = {
            "doc_content": doc.content,
            "num_questions": num_questions,
            "example_questions": example_questions,
        }
        resp = self._request_post("/managed-evals/generate-questions", request_json)

        _raise_for_status(resp)

        response_json = resp.json()
        if "questions" not in response_json or "error" in response_json:
            raise ValueError(f"Invalid response: {response_json}")
        return [
            entities.SyntheticQuestion(
                question=question,
                source_doc_uri=doc.doc_uri,
                source_context=doc.content,
            )
            for question in response_json["questions"]
        ]

    def generate_answer(
        self,
        *,
        question: entities.SyntheticQuestion,
        answer_types: Collection[entities.SyntheticAnswerType],
    ) -> entities.SyntheticAnswer:
        """
        Generate synthetic answer for the given question.
        """
        request_json = {
            "question": question.question,
            "context": question.source_context,
            "answer_types": [str(answer_type) for answer_type in answer_types],
        }
        resp = self._request_post("/managed-evals/generate-answer", request_json)

        _raise_for_status(resp)

        response_json = resp.json()
        return entities.SyntheticAnswer(
            question=question,
            synthetic_ground_truth=response_json.get("synthetic_ground_truth"),
            synthetic_grading_notes=response_json.get("synthetic_grading_notes"),
            synthetic_minimal_facts=response_json.get("synthetic_minimal_facts"),
        )
