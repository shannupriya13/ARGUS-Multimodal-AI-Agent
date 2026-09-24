from rag.rag_service import answer_from_document


vector_store_path = "tests/vector_store.json"

question = "What are the main areas I need to improve?"

result = answer_from_document(
    question,
    vector_store_path,
    top_k=2
)

print("\n===== ARGUS RAG ANSWER =====")
print("\nANSWER:")
print(result["answer"])

print("\nSOURCES:")
for i, source in enumerate(result["sources"]):
    print(f"\n--- SOURCE {i + 1} ---")
    print("Similarity:", round(source["similarity"], 4))
    print(source["text"][:500])