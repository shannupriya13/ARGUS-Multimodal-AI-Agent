from rag.document_loader import load_pdf, split_text


pdf_path = "tests/test_document.pdf"

text = load_pdf(pdf_path)
chunks = split_text(text)

print("\n===== ARGUS CHUNKING TEST =====")
print("Total characters:", len(text))
print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks[:3]):
    print(f"\n--- CHUNK {i + 1} ---")
    print(chunk[:500])