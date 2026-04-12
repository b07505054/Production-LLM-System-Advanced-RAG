import json

from app.eval.runner import run_retrieval_comparison
from app.eval.test_data import load_demo_eval_documents


if __name__ == "__main__":
    load_demo_eval_documents()

    dataset_path = "data/eval/retrieval_eval_dataset.jsonl"
    summary = run_retrieval_comparison(dataset_path)

    print(json.dumps(summary.model_dump(), indent=2, ensure_ascii=False))