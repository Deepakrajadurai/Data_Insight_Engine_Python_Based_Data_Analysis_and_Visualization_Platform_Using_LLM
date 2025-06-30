# chunker.py
import os
import json

INPUT_FOLDER = "data/cleaned_texts"
OUTPUT_FOLDER = "data/chunks"

CHUNK_SIZE = 500  # number of words per chunk

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def chunk_text(text, chunk_size=CHUNK_SIZE):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def process_all_cleaned_json():
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(".json"):
            input_path = os.path.join(INPUT_FOLDER, filename)
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            cleaned_text = data.get("cleaned_text")
            if not cleaned_text:
                print(f"⚠️ Skipping {filename} (no 'cleaned_text')")
                continue

            chunks = chunk_text(cleaned_text)
            chunk_data = {
                "filename": data["filename"],
                "num_chunks": len(chunks),
                "chunks": chunks
            }

            output_path = os.path.join(OUTPUT_FOLDER, filename)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(chunk_data, f, ensure_ascii=False, indent=2)

            print(f"✅ Chunked: {filename} → {len(chunks)} chunks")

if __name__ == "__main__":
    process_all_cleaned_json()
