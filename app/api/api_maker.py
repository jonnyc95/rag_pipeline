from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import os
from app.pdf_processing.pdf_loader import load_pdfs_from_folder
from app.pdf_processing.text_splitter import split_text
from app.embedding.embedding import embed_texts
from app.vector_store.vector_store import FaissStore
from app.QA.retrievalQA import answer_question
import logging
from typing import Optional

# === ENV KONFIGURATION ===
VECTOR_STORE_PATH = "faiss_index"
PDF_FOLDER = "data"
INDEX_PATH = os.path.join(VECTOR_STORE_PATH, "index.faiss")
META_PATH = os.path.join(VECTOR_STORE_PATH, "metadata.pkl")

# === Logging ===
logging.basicConfig(
    filename="system.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# === App Initialisieren ===
app = FastAPI(title="Wissenssystem API")

# === Laden oder initialisieren der Vektordatenbank ===
vector_store = FaissStore(dim=384, db_path=INDEX_PATH, metadata_path=META_PATH)
if os.path.exists(INDEX_PATH):
    vector_store.load()

# === Endpunkte ===

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(PDF_FOLDER, file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())
        logging.info(f"Hochgeladen: {file.filename}")
        
        # Neu verarbeiten
        documents = load_pdfs_from_folder(PDF_FOLDER)
        all_chunks = []
        for doc in documents:
            chunks = split_text(doc["text"])
            all_chunks.extend(chunks)
        embeddings = embed_texts(all_chunks)
        vector_store.add_embeddings(embeddings, all_chunks)
        vector_store.save()

        return {"status": "ok", "filename": file.filename}
    except Exception as e:
        logging.error(f"Fehler beim Upload: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/question")
async def ask_question(question: str = Form(...)):
    try:
        logging.info(f"Frage gestellt: {question}")
        response = answer_question(question, vector_store)
        return {"question": question, "answer": response}
    except Exception as e:
        logging.error(f"Fehler bei Frage: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/feedback")
async def feedback(
    question: str = Form(...),
    answer: str = Form(...),
    rating: int = Form(...),
    comment: Optional[str] = Form(None)
):
    try:
        feedback_entry = f"Frage: {question}\nAntwort: {answer}\nBewertung: {rating}/5\nKommentar: {comment or '-'}\n---\n"
        with open("feedback.log", "a", encoding="utf-8") as f:
            f.write(feedback_entry)
        logging.info("Feedback erhalten")
        return {"status": "Danke für dein Feedback!"}
    except Exception as e:
        logging.error(f"Feedback-Fehler: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
