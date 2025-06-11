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
ª   +---api
ª   ª   ª   api_maker.py #mit FastAPI
ª   ª   ª   
ª   ª   +---__pycache__
ª   ª           api_maker.cpython-310.pyc
ª   ª           
ª   +---embedding
ª   ª   ª   embedding.py
ª   ª   ª   
ª   ª   +---__pycache__
ª   ª           embedding.cpython-310.pyc
ª   ª           
ª   +---llm
ª   ª   ª   llm_loader.py
ª   ª   ª   
ª   ª   +---__pycache__
ª   ª           llm_loader.cpython-310.pyc
ª   ª           
ª   +---pdf_processing
ª   ª   ª   pdf_loader.py
ª   ª   ª   text_splitter.py
ª   ª   ª   
ª   ª   +---__pycache__
ª   ª           pdf_loader.cpython-310.pyc
ª   ª           text_splitter.cpython-310.pyc
ª   ª           
ª   +---QA
ª   ª   ª   retrievalQA.py
ª   ª   ª   
ª   ª   +---__pycache__
ª   ª           retrievalQA.cpython-310.pyc
ª   ª           
ª   +---vector_store
ª       ª   vector_store.py
ª       ª   
ª       +---__pycache__
ª               vector_store.cpython-310.pyc
ª               
+---data
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
+---models
ª       mistral-7b-instruct-v0.1.Q4_K_M.gguf
ª       
+---venv
    ª  ...


---------------------------------
# Start:
python main.py

# API starten:
uvicorn app.api.api_maker:app --reload


---------------------------------
# Docker verwenden

1. Build
docker build -t my-rag-app .

▶2. Starten
docker run -it --rm ^
  -v ${PWD}/models:/app/models ^
  -v ${PWD}/data:/app/data ^
  -v ${PWD}/faiss_index:/app/faiss_index ^
  --env-file .env ^
  my-rag-app

Unter Windows (PowerShell) mit ^ oder unter Linux/macOS mit \.

---------------------------------

# Umgebungsvariablen (.env)

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL_PATH=models/mistral-7b-instruct-v0.1.Q4_K_M.gguf
VECTOR_DB_PATH=faiss_index/index.faiss
CHUNK_SIZE=500
CHUNK_OVERLAP=50

---------------------------------

Requirements: 

faiss-cpu
sentence-transformers
transformers
datasets
PyMuPDF
python-dotenv

---------------------------------

Architektur:

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
