# app/main.py

import streamlit as st
import json
import os

# Paths to your processed data
SUMMARY_FOLDER = "data/summarized_chunks"
CLUSTER_PATH = "data/cluster_threads.json"
THREAD_PATH = "data/keyword_threads.json"
GRAPH_PATH = "data/topic_network.png"

st.set_page_config(page_title="📊 DIW Insight Engine", layout="wide")
st.title("📚 DIW Insight Engine")
st.markdown(
    "Analyze, cluster, and explore economic insights from German Institute for Economic Research (DIW) reports.")

# --- Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📄 Summaries", "🧠 Semantic Clusters", "🧵 Keyword Threads", "🌐 Topic Network"])

# --- Tab 1: Summaries ---
with tab1:
    st.header("📄 Document Summaries")
    summaries = []
    for fname in os.listdir(SUMMARY_FOLDER):
        if fname.endswith(".json"):
            with open(os.path.join(SUMMARY_FOLDER, fname), "r", encoding="utf-8") as f:
                data = json.load(f)
                summaries.append((data["filename"], data["chunks"]))

    for file, chunks in summaries:
        st.subheader(f"🗂️ {file}")
        for i, summary in enumerate(chunks):
            st.markdown(f"**Summary {i + 1}:** {summary}")

# --- Tab 2: Semantic Clusters ---
with tab2:
    st.header("🧠 Thematic Clusters")
    if os.path.exists(CLUSTER_PATH):
        with open(CLUSTER_PATH, "r", encoding="utf-8") as f:
            clusters = json.load(f)
        for cluster_id, cluster in clusters.items():
            st.subheader(f"🧭 Cluster {cluster_id}: {' '.join(cluster['keywords'])}")
            for s in cluster["summaries"][:5]:
                st.markdown(f"- {s}")
    else:
        st.warning("Clustering data not found.")

# --- Tab 3: Keyword Threads ---
with tab3:
    st.header("🧵 Threads by Keywords")
    if os.path.exists(THREAD_PATH):
        with open(THREAD_PATH, "r", encoding="utf-8") as f:
            threads = json.load(f)
        for kw, items in sorted(threads.items(), key=lambda x: -len(x[1])):
            st.subheader(f"🔑 {kw} ({len(items)} entries)")
            for item in items[:5]:
                st.markdown(f"- _{item['filename']}_: {item['summary']}")
    else:
        st.warning("Keyword thread data not found.")

# --- Tab 4: Topic Network ---
with tab4:
    st.header("🌐 Topic Network Graph")
    if os.path.exists(GRAPH_PATH):
        st.image(GRAPH_PATH, caption="Keyword Co-occurrence Network", use_column_width=True)
    else:
        st.warning("Network image not available.")
