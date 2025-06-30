import os
import json
from collections import defaultdict
from nltk.tokenize import word_tokenize

# Paths
INPUT_PATH = "Data/clustering_output.json"
LABELS_PATH = "data/cluster_labels.json"  # Optional, if available
OUTPUT_PATH = "data/keyword_threads.json"

# Load data
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Load cluster labels if they exist
labels = {}
if os.path.exists(LABELS_PATH):
    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        labels = json.load(f)

# Group by keywords
threads = defaultdict(list)
for item in data:
    keywords = item.get("keywords", [])
    for kw in keywords:
        threads[kw.lower()].append({
            "filename": item["filename"],
            "chunk_index": item["chunk_index"],
            "summary": item["summary"],
            "topic_label": labels.get(str(item["cluster"]), f"Cluster {item['cluster']}")
        })

# Save threads
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(threads, f, ensure_ascii=False, indent=2)

print("✅ Keyword threads saved to", OUTPUT_PATH)
