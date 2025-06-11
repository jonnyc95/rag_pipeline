# Speichert und sucht Vektoren mit FAISS

import faiss
import os
import pickle

class FaissStore:
    def __init__(self, dim, db_path="faiss_index/index.faiss", metadata_path="faiss_index/metadata.pkl"):
        self.index = faiss.IndexFlatL2(dim)         # L2-Distanzbasierter Index
        self.db_path = db_path
        self.metadata_path = metadata_path
        self.text_chunks = []

    def add_embeddings(self, embeddings, chunks):
        """
        Speichert neue Embeddings + zugehörige Texte.
        """
        self.index.add(embeddings)
        self.text_chunks.extend(chunks)

    def save(self):
        """
        Speichert Index + Metadaten auf die Festplatte.
        """
        faiss.write_index(self.index, self.db_path)
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.text_chunks, f)
        print(f"Gespeicherte Text-Chunks: {len(self.text_chunks)}")

    def load(self):
        """
        Lädt gespeicherten Index + Metadaten.
        """
        if os.path.exists(self.db_path):
            self.index = faiss.read_index(self.db_path)
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, "rb") as f:
                self.text_chunks = pickle.load(f)
        print(f"Geladene Text-Chunks: {len(self.text_chunks)}")

    def search(self, query_embedding, top_k=3):
        D, I = self.index.search(query_embedding, top_k)
        print("Such-Indizes:", I)  
        results = [self.text_chunks[i] for i in I[0] if i < len(self.text_chunks)]
        print(f"Anzahl gefundener Chunks: {len(results)}")
        return results

