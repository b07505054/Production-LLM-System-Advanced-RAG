from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForFeatureExtraction
import numpy as np

class ONNXEmbedder:
    def __init__(self, model_path="model/onnx"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = ORTModelForFeatureExtraction.from_pretrained(model_path)

    def embed_text(self, text: str):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.detach().numpy()[0].tolist()

    def embed_texts(self, texts: list[str]):
        return [self.embed_text(t) for t in texts]


import os

backend = os.getenv("EMBEDDER_BACKEND", "onnx_fp32")

if backend == "onnx_int8":
    from app.retrieval.embedder_onnx_int8 import ONNXInt8Embedder
    embedder = ONNXInt8Embedder()

else:
    embedder = ONNXEmbedder()