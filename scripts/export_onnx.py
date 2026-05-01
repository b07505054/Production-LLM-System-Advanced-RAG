from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

model.save("model/miniLM")

print("Model saved to model/miniLM")