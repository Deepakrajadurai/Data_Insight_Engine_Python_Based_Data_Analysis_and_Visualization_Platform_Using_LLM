import os
import json

INPUT_FOLDER = "data/chunks"
OUTPUT_FOLDER = "data/summarized_chunks"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def naive_summarize(text, max_sentences=2):
    sentences = text.split('.')
    clean_sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    return ". ".join(clean_sentences[:max_sentences]) + "."

def summarize_all_chunks():
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith(".json"):
            with open(os.path.join(INPUT_FOLDER, filename), "r", encoding="utf-8") as f:
                data = json.load(f)

            chunks = data.get("chunks", [])
            summaries = [naive_summarize(chunk) for chunk in chunks]
            data["summaries"] = summaries

            with open(os.path.join(OUTPUT_FOLDER, filename), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"✅ Summarized: {filename}")

if __name__ == "__main__":
    summarize_all_chunks()
