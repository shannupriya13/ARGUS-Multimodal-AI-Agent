from dotenv import load_dotenv
from google import genai
import json

load_dotenv()

client = genai.Client()


def create_embedding(text: str):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values


def create_embeddings(chunks: list[str]):
    embeddings = []

    for chunk in chunks:
        embedding = create_embedding(chunk)
        embeddings.append(embedding)

    return embeddings


def save_vector_store(chunks: list[str], embeddings: list[list[float]], file_path: str):
    data = []

    for chunk, embedding in zip(chunks, embeddings):
        data.append({
            "text": chunk,
            "embedding": embedding
        })

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file)


def load_vector_store(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

import math


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def search_vector_store(
    query: str,
    vector_store: list,
    top_k: int = 3
):
    query_embedding = create_embedding(query)

    results = []

    for item in vector_store:
        similarity = cosine_similarity(
            query_embedding,
            item["embedding"]
        )

        results.append({
            "text": item["text"],
            "similarity": similarity
        })

    results.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    return results[:top_k]