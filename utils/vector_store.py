import numpy as np
from utils.embeddings import get_embedding

vector_store = []

def add_document(doc_id, text):
    embedding = get_embedding(text)
    vector_store.append((doc_id, embedding, text))

def search(query, k=5):
    query_vector = get_embedding(query)
    sims = []
    for doc_id, emb, text in vector_store:
        sim = np.dot(query_vector, emb) / (np.linalg.norm(query_vector) * np.linalg.norm(emb))
        sims.append((sim, text))
    sims.sort(reverse=True, key=lambda x: x[0])
    return [t for _, t in sims[:k]]
