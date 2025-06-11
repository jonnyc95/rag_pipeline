import os
from dotenv import load_dotenv
from app.pdf_processing.pdf_loader import load_pdfs_from_folder
from app.pdf_processing.text_splitter import split_text
from app.embedding.embedding import embed_texts
from app.vector_store.vector_store import FaissStore
from app.QA.retrievalQA import answer_question

# .env-Datei laden
load_dotenv()

# Konfiguration aus Umgebungsvariablen
PDF_FOLDER = os.getenv("PDF_FOLDER", "data")
FAISS_FOLDER = os.getenv("FAISS_FOLDER", "faiss_index")
FAISS_INDEX_PATH = os.path.join(FAISS_FOLDER, "index.faiss")
FAISS_META_PATH = os.path.join(FAISS_FOLDER, "metadata.pkl")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "False") == "True"        # Pfad zu den zugehörigen Text-Chunks

def build_knowledge_base():
    """
    Diese Funktion erstellt die Wissensbasis:
    - Sie lädt alle PDFs aus dem Datenordner
    - Extrahiert Textinhalte
    - Zerlegt diese in kleinere Textabschnitte (Chunks)
    - Erstellt Embeddings dieser Abschnitte
    - Speichert die Vektoren in einer FAISS-Datenbank
    """
    print("Lade und verarbeite PDFs...")

    # Texte aus allen PDFs extrahieren
    documents = load_pdfs_from_folder(PDF_FOLDER)

    all_chunks = []

    # Jeder Dokumenttext wird in kleinere Chunks aufgeteilt
    for doc in documents:
        chunks = split_text(doc["text"])
        all_chunks.extend(chunks)

    if not all_chunks:
        print("Keine Texte gefunden zum Verarbeiten.")
        return

    print(f"Insgesamt {len(all_chunks)} Text-Chunks erstellt.")

    # Für jeden Chunk wird ein semantischer Vektor (Embedding) berechnet
    print("Berechne Embeddings...")
    embeddings = embed_texts(all_chunks)

    # Initialisiere FAISS-Datenbank und speichere die Vektoren mit zugehörigen Texten
    print("Speichere Vektoren mit FAISS...")
    vector_store = FaissStore(
        dim=len(embeddings[0]),
        db_path=FAISS_INDEX_PATH,
        metadata_path=FAISS_META_PATH
    )
    vector_store.add_embeddings(embeddings, all_chunks)
    vector_store.save()

    print("Wissensbasis erfolgreich erstellt.")

def ask_questions():
    """
    Diese Funktion startet eine interaktive Schleife, um Fragen zu stellen:
    - Die gespeicherte FAISS-Datenbank wird geladen
    - Der Benutzer gibt eine Frage ein
    - Das System sucht nach den relevantesten Textabschnitten
    - Das lokale LLM generiert eine Antwort auf Basis dieser Informationen
    """
    if not os.path.exists(FAISS_INDEX_PATH):
        print("Kein FAISS-Index gefunden. Bitte zuerst die Wissensbasis aufbauen.")
        return

    print("Lade Vektordatenbank...")
    vector_store = FaissStore(
        dim=384,  # Dimension des genutzten SentenceTransformer-Embeddings
        db_path=FAISS_INDEX_PATH,
        metadata_path=FAISS_META_PATH
    )
    vector_store.load()

    # Endlosschleife für interaktive Fragenbeantwortung
    while True:
        user_input = input("\nDeine Frage (oder 'exit' zum Beenden): ")
        if user_input.lower().strip() == "exit":
            print("Auf Wiedersehen.")
            break

        print("Frage wurde gestellt:", user_input)
        response = answer_question(user_input, vector_store)
        print("Antwort erhalten:", response)

# Hauptlogik beim Start des Programms
if __name__ == "__main__":
    # Wenn kein FAISS-Index existiert, wird die Wissensbasis neu aufgebaut
    if not os.path.exists(FAISS_INDEX_PATH):
        build_knowledge_base()

    # Starte interaktiven Fragenmodus
    ask_questions()
