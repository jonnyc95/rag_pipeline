# Kombination aus Retrieval (semantisch ähnlichster Kontext) + Antwortgenerierung via LLM

from app.embedding.embedding import embed_texts
#from app.vector_store.vector_store import FaissStore
from app.llm.llm_loader import generate_answer  # Lokales Modell
import numpy as np

def answer_question(question, vector_store):
    """
    1. Embedding der Frage
    2. Ähnlichste Textabschnitte abrufen
    3. Prompt bauen
    4. Antwort generieren via Mistral (lokal)
    """
    print("Frage:", question)
    query_embedding = embed_texts([question])
    query_embedding = np.array(query_embedding).astype("float32").reshape(1, -1)
    print("Query-Embedding-Shape:", query_embedding.shape)


    relevant_chunks = vector_store.search(query_embedding, top_k=3)

    # Prompt für das lokale Modell
    context = "\n\n".join(relevant_chunks)
    prompt = f"""Beantworte die folgende Frage auf Basis des untenstehenden Kontexts in eigenen Worten, klar und verständlich, so als würdest du es jemandem erklären, der kein Experte ist. Verwende kein Copy-Paste aus dem Text, sondern fasse den Inhalt logisch zusammen:

Kontext:
{context}

Frage: {question}
Antwort:"""

    print("Prompt an LLM:\n", prompt)

    answer = generate_answer(prompt)
    return answer
