from pathlib import Path

import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer


class ONNXInt8Embedder:
    def __init__(self, model_dir: str = "model/onnx_int8") -> None:
        self.model_dir = Path(model_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(str(self.model_dir))

        self.session = ort.InferenceSession(
            str(self.model_dir / "model_int8.onnx"),
            providers=["CPUExecutionProvider"],
        )

    def _mean_pooling(self, token_embeddings: np.ndarray, attention_mask: np.ndarray) -> np.ndarray:
        input_mask_expanded = np.expand_dims(attention_mask, axis=-1)
        sum_embeddings = np.sum(token_embeddings * input_mask_expanded, axis=1)
        sum_mask = np.clip(np.sum(input_mask_expanded, axis=1), a_min=1e-9, a_max=None)
        return sum_embeddings / sum_mask

    def _normalize(self, embeddings: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        return embeddings / np.clip(norms, a_min=1e-9, a_max=None)

    def embed_text(self, text: str) -> list[float]:
        return self.embed_texts([text])[0]

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            return_tensors="np",
        )

        ort_inputs = {
            "input_ids": inputs["input_ids"],
            "attention_mask": inputs["attention_mask"],
        }

        if "token_type_ids" in inputs:
            ort_inputs["token_type_ids"] = inputs["token_type_ids"]

        outputs = self.session.run(None, ort_inputs)

        token_embeddings = outputs[0]
        embeddings = self._mean_pooling(token_embeddings, inputs["attention_mask"])
        embeddings = self._normalize(embeddings)

        return embeddings.tolist()