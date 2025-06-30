# classify.py
import os
import json

INPUT_FOLDER = "data/chunks"
OUTPUT_FOLDER = "data/classified_chunks"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Define topic keywords (lowercase!)
TOPIC_KEYWORDS = {
    "Housing & Construction": ["residential", "construction", "building permits", "renovation"],
    "Green Energy & Heat Transition": ["energy", "heat pump", "decarbon", "co2", "climate"],
    "Migration & Labor": ["migration", "refugee", "integration", "employment", "labor market"],
    "Economic Outlook": ["inflation", "gdp", "forecast", "interest rates", "economy"],
    "Public Investment & Infrastructure": ["infrastructure", "public investment", "transport", "railway", "school"]
}

def classify_chunk(text):
    labels = set()
    lowered = text.lower()
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(kw in lowered for kw in keywords):
            labels.add(topic)
    return list(labels) if labels else ["Uncategorized"]

def classify_all_chunks():
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith(".json"):
            with open(os.path.join(INPUT_FOLDER, filename), "r", encoding="utf-8") as f:
                data = json.load(f)

            chunk_labels = [classify_chunk(chunk) for chunk in data["chunks"]]
            data["topics"] = chunk_labels

            output_path = os.path.join(OUTPUT_FOLDER, filename)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Classified: {filename}")

if __name__ == "__main__":
    classify_all_chunks()
