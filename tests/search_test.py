from rag.vector_store import load_vector_store, search_vector_store


vector_store_path = "tests/vector_store.json"

vector_store = load_vector_store(vector_store_path)

query = "What are the areas I need to improve?"

results = search_vector_store(
    query,
    vector_store,
    top_k=2
)

print("\n===== ARGUS SEMANTIC SEARCH =====")
print("Query:", query)

for i, result in enumerate(results):
    print(f"\n--- RESULT {i + 1} ---")
    print("Similarity:", round(result["similarity"], 4))
    print("Text:")
    print(result["text"][:1000])