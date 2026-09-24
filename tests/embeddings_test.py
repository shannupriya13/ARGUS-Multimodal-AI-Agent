from rag.document_loader import load_pdf, split_text
from rag.vector_store import create_embeddings


pdf_path = "tests/test_document.pdf"

text = load_pdf(pdf_path)
chunks = split_text(text)

embeddings = create_embeddings(chunks)

print("\n===== ARGUS MULTI-CHUNK EMBEDDING TEST =====")
print("Total chunks:", len(chunks))
print("Total embeddings:", len(embeddings))

for i, embedding in enumerate(embeddings):
    print(f"Chunk {i + 1} embedding dimensions:", len(embedding))