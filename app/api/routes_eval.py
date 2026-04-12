from fastapi import APIRouter, HTTPException

from app.schemas.eval_api import EvalRequest
from app.schemas.eval import RetrievalComparisonSummary
from app.eval.runner import run_retrieval_comparison
from app.eval.test_data import load_demo_eval_documents


router = APIRouter(prefix="/evaluate", tags=["evaluate"])


@router.post("", response_model=RetrievalComparisonSummary)
def evaluate_retrieval(payload: EvalRequest) -> RetrievalComparisonSummary:
    try:
        if payload.load_demo_data:
            load_demo_eval_documents()

        summary = run_retrieval_comparison(payload.dataset_path)
        return summary

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "EVAL_DATASET_NOT_FOUND",
                "message": str(exc),
            },
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "EVALUATION_ERROR",
                "message": str(exc),
            },
        ) from exc