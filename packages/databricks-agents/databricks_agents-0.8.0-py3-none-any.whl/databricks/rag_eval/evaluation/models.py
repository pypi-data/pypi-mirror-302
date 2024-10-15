"""
This module contains helper functions for invoking the model to be evaluated.
"""

import logging
import uuid
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

import mlflow
import mlflow.entities as mlflow_entities
import mlflow.pyfunc.context as pyfunc_context

from databricks.rag_eval.evaluation import entities, traces
from databricks.rag_eval.utils import input_output_utils
from databricks.rag_eval.utils.collection_utils import deep_update

_MODEL_INPUT__MESSAGES_COL = "messages"
_MODEL_INPUT__ROLE_COL = "role"
_MODEL_INPUT__CONTENT_COL = "content"
_MODEL_INPUT__USER_ROLE = "user"
_MODEL_INPUT__RETURN_TRACE_FLAG = {
    "databricks_options": {
        "return_trace": True,
    }
}


_logger = logging.getLogger(__name__)


@dataclass
class ModelResult:
    """
    The result of invoking the model.
    """

    response: Optional[str]
    retrieval_context: Optional[entities.RetrievalContext]
    trace: Optional[mlflow_entities.Trace]
    error_message: Optional[str]

    @classmethod
    def from_outputs(
        cls,
        *,
        response: Optional[str],
        retrieval_context: Optional[entities.RetrievalContext],
        trace: Optional[mlflow_entities.Trace],
    ) -> "ModelResult":
        """Build a normal model result with response and retrieval context."""
        return cls(
            response=response,
            retrieval_context=retrieval_context,
            trace=trace,
            error_message=None,
        )

    @classmethod
    def from_error_message(cls, error_message: str) -> "ModelResult":
        """Build a model result with an error message."""
        return cls(
            response=None,
            retrieval_context=None,
            trace=None,
            error_message=error_message,
        )


def invoke_model(
    model: mlflow.pyfunc.PyFuncModel, eval_item: entities.EvalItem
) -> ModelResult:
    """
    Invoke the model with a request to get a model result.

    :param model: The model to invoke.
    :param eval_item: The eval item containing the request.
    :return: The model result.
    """
    try:
        model_input = _to_model_input_format(eval_item.raw_request)
        model_input = _set_include_trace(model_input)
        # Invoke the model
        model_output, trace = _model_predict_with_trace(model, model_input)
        # Get the response from the model output
        try:
            response = input_output_utils.output_to_string(model_output)
        except ValueError as e:
            return ModelResult.from_error_message(
                f"Failed to parse the model output: {model_output}. {e!r}"
            )
        retrieval_context = traces.extract_retrieval_context_from_trace(trace)

        model_result = ModelResult.from_outputs(
            response=response,
            retrieval_context=retrieval_context,
            trace=trace,
        )
        return model_result

    except Exception as e:
        return ModelResult.from_error_message(str(e))


def _to_model_input_format(request: Any) -> Dict[str, Any]:
    """
    Convert the request string to the format expected by the model.

    :param request: The request string
    :return: The model input format
    """
    if isinstance(request, str):
        # For backward compatibility, we convert input strings into ChatCompletionRequests
        # before invoking the model.
        return {
            _MODEL_INPUT__MESSAGES_COL: [
                {
                    _MODEL_INPUT__ROLE_COL: _MODEL_INPUT__USER_ROLE,
                    _MODEL_INPUT__CONTENT_COL: request,
                },
            ],
        }
    else:
        return request


def _set_include_trace(model_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Set the flag to include trace in the model input.

    :param model_input: The model input
    :return: The model input with the flag set
    """
    return deep_update(model_input, _MODEL_INPUT__RETURN_TRACE_FLAG)


def _model_predict_with_trace(
    model: mlflow.pyfunc.PyFuncModel, model_input: Dict
) -> Tuple[input_output_utils.ModelOutput, mlflow_entities.Trace]:
    """
    Invoke the model to get output and trace.

    :param model: The langchain model
    :param model_input: The model input
    :return: The response and the retrieval context
    """
    try:
        # Use a random UUID as the context ID to avoid conflicts with other evaluations on the same set of questions
        context_id = str(uuid.uuid4())
        with pyfunc_context.set_prediction_context(
            pyfunc_context.Context(context_id, is_evaluate=True)
        ):
            model_output = model.predict(model_input)
            trace = input_output_utils.extract_trace_from_output(
                model_output
            ) or mlflow.get_trace(context_id)
        return model_output, trace
    except Exception as e:
        raise ValueError(f"Fail to invoke the model with {model_input}. {e!r}")
