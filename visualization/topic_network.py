# visualization/topic_network.py

import json
import networkx as nx
import matplotlib.pyplot as plt

# Paths
THREADS_PATH = "data/keyword_threads.json"
OUTPUT_PATH = "data/topic_network.png"

# Load keyword threads
with open(THREADS_PATH, "r", encoding="utf-8") as f:
    threads = json.load(f)

# Initialize graph
G = nx.Graph()

# Build nodes and weighted edges
for keyword, items in threads.items():
    G.add_node(keyword, size=len(items))

    # Create co-occurrence links
    seen_docs = set()
    for entry in items:
        doc = entry["filename"]
        if doc not in seen_docs:
            seen_docs.add(doc)
            for other_kw in threads:
                if other_kw != keyword and any(e["filename"] == doc for e in threads[other_kw]):
                    G.add_edge(keyword, other_kw)

# Draw graph
plt.figure(figsize=(12, 10))
pos = nx.spring_layout(G, k=0.4)
sizes = [G.nodes[n]["size"] * 50 for n in G.nodes]
nx.draw_networkx_nodes(G, pos, node_size=sizes, node_color='skyblue')
nx.draw_networkx_edges(G, pos, alpha=0.3)
nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

plt.title("🧭 DIW Topic Network", fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.savefig(OUTPUT_PATH)
print(f"✅ Topic network saved to {OUTPUT_PATH}")
