import os
from PyPDF2 import PdfReader

def load_pdfs_from_folder(folder_path):
    texts = []
    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        text = ""

        if filename.endswith(".pdf"):
            from PyPDF2 import PdfReader
            reader = PdfReader(path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

        #V1
        elif filename.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

        if text.strip():
            texts.append({"filename": filename, "text": text})
    return texts
