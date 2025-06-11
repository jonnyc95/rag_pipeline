import os

# Pfad zum Projektverzeichnis (das aktuelle Verzeichnis)
project_dir = "app"
output_file = "all_code_combined.txt"

with open(output_file, "w", encoding="utf-8") as outfile:
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                outfile.write(f"# === Datei: {file_path} ===\n\n")
                with open(file_path, "r", encoding="utf-8") as f:
                    outfile.write(f.read())
                    outfile.write("\n\n")
print(f"✅ Alle Python-Dateien aus '{project_dir}' wurden in '{output_file}' zusammengeführt.")
