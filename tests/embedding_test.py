from rag.vector_store import create_embedding


text = "ARGUS is a multimodal AI agent."

embedding = create_embedding(text)

print("\n===== ARGUS EMBEDDING TEST =====")
print("Embedding created successfully")
print("Vector dimensions:", len(embedding))
print("First 5 values:", embedding[:5])