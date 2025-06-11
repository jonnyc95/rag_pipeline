# Lädt ein lokal laufendes Mistral 7B-Modell via llama-cpp

from llama_cpp import Llama

# Initialisiere das Modell (GGUF-Datei muss vorhanden sein)
llm = Llama(
    model_path="models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",  # Pfad zur Modell-Datei
    n_ctx=4096,
    n_threads=8,   # CPU anpassen?
    n_gpu_layers=0 # 0 =rein CPU-basiert
)

def generate_answer(prompt):
    """
    Übergibt den Prompt an das Modell und gibt die Antwort zurück.
    """
    response = llm(prompt, max_tokens=512, stop=["</s>"])
    return response["choices"][0]["text"].strip()
