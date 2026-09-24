from rag.document_loader import load_pdf


pdf_path = "tests/test_document.pdf"

text = load_pdf(pdf_path)

print("\n===== ARGUS PDF EXTRACTION =====\n")
print(text[:3000])