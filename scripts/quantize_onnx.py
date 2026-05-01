from pathlib import Path
from onnxruntime.quantization import quantize_dynamic, QuantType

input_model = Path("model/onnx/model.onnx")
output_model = Path("model/onnx_int8/model_int8.onnx")

output_model.parent.mkdir(parents=True, exist_ok=True)

quantize_dynamic(
    model_input=str(input_model),
    model_output=str(output_model),
    weight_type=QuantType.QInt8,
)

print(f"Quantized model saved to {output_model}")