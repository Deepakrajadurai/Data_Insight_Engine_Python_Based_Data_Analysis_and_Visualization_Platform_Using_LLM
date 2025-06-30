# narrative_builder.py
import os
import json
from collections import defaultdict, Counter
import re

INPUT_PATH = "data/clustering_output.json"
OUTPUT_PATH = "data/cluster_threads.json"

def extract_keywords(text, stopwords, top_n=10):
    words = re.findall(r'\b\w+\b', text.lower())
    words = [w for w in words if w not in stopwords and len(w) > 3]
    freq = Counter(words)
    return [word for word, _ in freq.most_common(top_n)]

def build_cluster_threads(data, stopwords):
    clusters = defaultdict(list)
    for item in data:
        if item["cluster"] != "noise":
            clusters[item["cluster"]].append(item)

    result = []
    for cluster_id, items in clusters.items():
        all_text = " ".join(item["text"] for item in items)
        keywords = extract_keywords(all_text, stopwords)
        label = ", ".join(keywords[:3]).title()
        result.append({
            "cluster_id": cluster_id,
            "topic_label": label,
            "key_terms": keywords,
            "summaries": [
                {
                    "filename": item["filename"],
                    "chunk_index": item["chunk_index"],
                    "summary": item["text"]
                }
                for item in items
            ]
        })

    return result

if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        clustered_data = json.load(f)

    STOPWORDS = set([
        "the", "and", "for", "with", "that", "this", "from", "are", "was",
        "has", "have", "will", "not", "but", "also", "more", "can", "than",
        "other", "such", "been", "which", "may", "all", "its", "these", "their",
        "one", "into", "only", "per", "some", "most", "used", "use", "they"
    ])

    cluster_threads = build_cluster_threads(clustered_data, STOPWORDS)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(cluster_threads, f, indent=2, ensure_ascii=False)

    print(f"✅ Cluster narratives saved to {OUTPUT_PATH}")
