import json
from pathlib import Path
from typing import List

from app.eval.retrieval_eval import compare_retrieval_modes, evaluate_dataset
from app.schemas.eval import (
    RetrievalEvalExample,
    RetrievalEvalSummary,
    RetrievalComparisonSummary,
)


def load_eval_dataset(file_path: str) -> List[RetrievalEvalExample]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Evaluation dataset not found: {file_path}")

    examples = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            row = json.loads(line)
            examples.append(RetrievalEvalExample(**row))

    return examples


def run_retrieval_eval(
    file_path: str,
    use_reranker: bool = False,
) -> RetrievalEvalSummary:
    examples = load_eval_dataset(file_path)
    return evaluate_dataset(examples, use_reranker=use_reranker)


def run_retrieval_comparison(file_path: str) -> RetrievalComparisonSummary:
    examples = load_eval_dataset(file_path)
    return compare_retrieval_modes(examples)