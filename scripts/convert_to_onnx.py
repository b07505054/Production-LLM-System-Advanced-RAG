from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer

model_id = "model/miniLM"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = ORTModelForFeatureExtraction.from_pretrained(model_id, export=True)

model.save_pretrained("model/onnx")
tokenizer.save_pretrained("model/onnx")

print("ONNX model exported!")