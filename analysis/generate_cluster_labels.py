# analysis/generate_cluster_labels.py
import os
import json
from collections import Counter, defaultdict

CLUSTERING_PATH = "data/clustering_output.json"
SUMMARY_FOLDER = "data/summarized_chunks"
OUTPUT_PATH = "data/cluster_threads.json"

# Load clustering results
with open(CLUSTERING_PATH, "r", encoding="utf-8") as f:
    cluster_data = json.load(f)

# Build lookup: (filename, chunk_index) -> summary
summary_lookup = {}
for fname in os.listdir(SUMMARY_FOLDER):
    if fname.endswith(".json"):
        with open(os.path.join(SUMMARY_FOLDER, fname), "r", encoding="utf-8") as f:
            data = json.load(f)
            filename = data["filename"]
            for i, summary in enumerate(data["chunks"]):
                summary_lookup[(filename, i)] = summary

# Group summaries by cluster
clusters = defaultdict(list)
for item in cluster_data:
    key = (item["filename"], item["chunk_index"])
    summary = summary_lookup.get(key)
    if summary:
        clusters[item["cluster"]].append(summary)

# Extract top words per cluster
cluster_threads = {}
for cluster_id, summaries in clusters.items():
    words = " ".join(summaries).lower().split()
    top_words = [word for word, _ in Counter(words).most_common(5)]
    cluster_threads[cluster_id] = {
        "keywords": top_words,
        "summaries": summaries
    }

# Save result
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(cluster_threads, f, indent=2, ensure_ascii=False)

print("✅ Cluster threads saved to", OUTPUT_PATH)
