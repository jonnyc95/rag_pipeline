ReadME: 
# RAG Pipeline (Retrieval-Augmented Generation)

Diese Anwendung kombiniert Vektorsuche mit einem leistungsfähigen Sprachmodell (LLM), um Fragen auf Basis von Dokumenten zu beantworten. Sie basiert auf einer modularen Architektur mit Docker, FAISS, HuggingFace und Mistral 7B.

---------------------------------

# Features

- ✅ LLM (Mistral 7B) lokal ausgeführt
- ✅ FAISS Vektordatenbank
- ✅ Kontextbasierte Fragebeantwortung
- ✅ Dockerisiert für einfache Ausführung

---------------------------------

# Projektstruktur
RAG Pipeline
ª   .dockerignore
ª   .env
ª   Dockerfile
ª   feedback.log
ª   main.py
ª   projektstruktur.txt
ª   README.txt
ª   requirements.txt
ª   structure.txt
ª   system.log
ª   
+---app
ª   +---api # FastAPI Endpunkte
ª   ª   ª   api_maker.py 
ª   ª   ª   
ª   ª   +---__pycache__
ª   ª           api_maker.cpython-310.pyc
ª   ª           
ª   +---embedding # SentenceTransformer Embedding
ª   ª   ª   embedding.py 
ª   ª   ª   
ª   ª   +---__pycache__
ª   ª           embedding.cpython-310.pyc
ª   ª           
ª   +---llm # LLM-Integration (Mistral via llama-cpp)
ª   ª   ª   llm_loader.py 
ª   ª   ª   
ª   ª   +---__pycache__
ª   ª           llm_loader.cpython-310.pyc
ª   ª           
ª   +---pdf_processing # PDF-Laden & Chunking
ª   ª   ª   pdf_loader.py
ª   ª   ª   text_splitter.py
ª   ª   ª   
ª   ª   +---__pycache__
ª   ª           pdf_loader.cpython-310.pyc
ª   ª           text_splitter.cpython-310.pyc
ª   ª           
ª   +---QA # Fragebeantwortung (RAG)
ª   ª   ª   retrievalQA.py
ª   ª   ª   
ª   ª   +---__pycache__
ª   ª           retrievalQA.cpython-310.pyc
ª   ª           
ª   +---vector_store # FastAPI Endpunkte
ª       ª   vector_store.py
ª       ª   
ª       +---__pycache__
ª               vector_store.cpython-310.pyc
ª               
+---data # Beispiel-Dokumente (PDF, TXT)
ª       BMF_2013_07_24.pdf
ª       BMF_2014_01_13_AªÛnderung_von_2013_07_24.pdf
ª       BMF_2017_12_06.pdf
ª       BMF_2017_12_21.pdf
ª       BMF_2019_08_08_AªÛnderung_von_2017_12_06.pdf
ª       BMF_2020_02_17_AªÛnderung_von_2017_12_21.pdf
ª       BMF_2022_02_11_AªÛnderung_von_2017_12_21_und_2020_02_17.pdf
ª       BMF_2022_03_18_AªÛnderung_von_2021_08_21.pdf
ª       BMF_2023_10_05.pdf
ª       estg.txt
ª       
+---faiss_index
ª       index.faiss
ª       index.pkl
ª       metadata.pkl
ª       
+---models # Lokales GGUF-Modell (nicht im Repo!)
ª       mistral-7b-instruct-v0.1.Q4_K_M.gguf #von HuggingFace
ª       
+---venv
    ª  ...

# Virtuelle Umgebung (optional, empfohlen)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Abhängigkeiten installieren
pip install -r requirements.txt
Achtung: Für llama-cpp muss dein System C++ unterstützen (C++ Buildtools für LLM Mode)

# Ausführen:
python main.py 
oder direkt via FastAPI starten im nächsten Schritt (siehe "API starten")

# API starten:
uvicorn app.api.api_maker:app --reload
mit: POST /upload, POST /question, POST /feedback
Hinweis: Feedback wird lokal in feedback.log gespeichert

# Technologien & Bibliotheken
FastAPI – für das API-Backend
SentenceTransformers – für Text-Embeddings
FAISS – schnelle Ähnlichkeitssuche
llama-cpp-python – um Mistral 7B lokal laufen zu lassen
PyPDF2, langchain – für PDF-Verarbeitung & Chunking

# Docker verwenden

1. Build
docker build -t rag_pipeline .
2. Starten
ddocker run -p 8000:8000 rag-pipeline

# Umgebungsvariablen (.env)

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL_PATH=models/mistral-7b-instruct-v0.1.Q4_K_M.gguf
VECTOR_DB_PATH=faiss_index/index.faiss
CHUNK_SIZE=500
CHUNK_OVERLAP=50

# Requirements: 
faiss-cpu
sentence-transformers
transformers
datasets
PyMuPDF
python-dotenv


# Architektur:
+----------------+
|  Dokumente     |
+----------------+
        ↓
+----------------+
|  Text Splitter |
+----------------+
        ↓
+----------------+
| Embedding-Modell |
+----------------+
        ↓
+----------------+
| FAISS Index   |
+----------------+
        ↓
+----------------+
|  LLM (Mistral) |
+----------------+
        ↓
|  Antwort  |
+-----------+


Bei Fragen gerne melden!

UI ist noch in Bearbeitung! (Bonus)

# Impressum / Rechtliches
Hinweis: Die bereitgestellten Dokumente und Inhalte dienen ausschließlich Demonstrations- und Forschungszwecken. Dieses System ersetzt keine juristische Beratung.
