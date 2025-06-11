from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/multilingual-e5-small")

def embed_texts(texts):
    inputs = [f"passage: {text}" for text in texts]
    embeddings = model.encode(inputs, show_progress_bar=True)
    return embeddings