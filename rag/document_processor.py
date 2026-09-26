import os

from rag.document_loader import load_pdf, split_text
from rag.vector_store import create_embeddings, save_vector_store


def process_document(pdf_path: str, vector_store_path: str):

    text = load_pdf(pdf_path)

    if not text.strip():
        raise ValueError(
            "No readable text was found in the PDF."
        )

    chunks = split_text(text)

    if not chunks:
        raise ValueError(
            "Could not create document chunks."
        )

    embeddings = create_embeddings(chunks)

    os.makedirs(
        os.path.dirname(vector_store_path),
        exist_ok=True
    )

    save_vector_store(
        chunks,
        embeddings,
        vector_store_path
    )

    return {
        "chunks": len(chunks),
        "vector_store": vector_store_path
    }