# clustering.py
import os
import json
import numpy as np
import umap
import hdbscan
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt

INPUT_FOLDER = "data/summarized_chunks"
OUTPUT_PATH = "data/clustering_output.json"

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Collect all summaries and metadata
texts, metadata = [], []
for filename in os.listdir(INPUT_FOLDER):
    if filename.endswith(".json"):
        with open(os.path.join(INPUT_FOLDER, filename), "r", encoding="utf-8") as f:
            data = json.load(f)
            for i, chunk in enumerate(data["summaries"]):
                texts.append(chunk)
                metadata.append({
                    "filename": data["filename"],
                    "chunk_index": i
                })

# Generate embeddings
print("🔍 Generating embeddings...")
embeddings = model.encode(texts, show_progress_bar=True)

# Reduce dimensions with UMAP
print("📉 Applying UMAP dimensionality reduction...")
umap_model = umap.UMAP(n_neighbors=15, n_components=2, min_dist=0.1, metric='cosine')
umap_embeddings = umap_model.fit_transform(embeddings)

# Cluster using HDBSCAN
print("🧠 Performing HDBSCAN clustering...")
clusterer = hdbscan.HDBSCAN(min_cluster_size=5, metric='euclidean')
cluster_labels = clusterer.fit_predict(umap_embeddings)

# Save results
results = []
for i, text in enumerate(texts):
    results.append({
        "text": text,
        "filename": metadata[i]["filename"],
        "chunk_index": metadata[i]["chunk_index"],
        "umap_x": float(umap_embeddings[i, 0]),
        "umap_y": float(umap_embeddings[i, 1]),
        "cluster": int(cluster_labels[i]) if cluster_labels[i] != -1 else "noise"
    })

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# Optional: show scatter plot
plt.figure(figsize=(10, 8))
plt.scatter(umap_embeddings[:, 0], umap_embeddings[:, 1], c=cluster_labels, cmap='Spectral', s=10)
plt.title("UMAP + HDBSCAN Cluster Visualization")
plt.xlabel("UMAP 1")
plt.ylabel("UMAP 2")
plt.grid(True)
plt.tight_layout()
plt.savefig("data/cluster_plot.png")
print("✅ Clustering complete. Results saved.")
