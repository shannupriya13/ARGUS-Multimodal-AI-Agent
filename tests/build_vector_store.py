from rag.document_loader import load_pdf, split_text
from rag.vector_store import create_embeddings, save_vector_store


pdf_path = "tests/test_document.pdf"
vector_store_path = "tests/vector_store.json"


text = load_pdf(pdf_path)
chunks = split_text(text)

print("Creating embeddings...")

embeddings = create_embeddings(chunks)

save_vector_store(
    chunks,
    embeddings,
    vector_store_path
)

print("\n===== ARGUS VECTOR STORE =====")
print("Chunks stored:", len(chunks))
print("Vector store:", vector_store_path)
print("Status: SUCCESS")