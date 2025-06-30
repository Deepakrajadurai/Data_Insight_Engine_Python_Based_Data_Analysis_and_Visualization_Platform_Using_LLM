# app/pages/1_Summarization.py

import os
import json
import streamlit as st

SUMMARY_DIR = "Data/summarized_chunks"
CLASSIFIED_DIR = "Data/classified_chunks"

st.set_page_config(page_title="📄 DIW Summaries", layout="wide")
st.title("📄 DIW Weekly Report Summaries")
st.markdown("Explore categorized summaries from DIW economic reports based on thematic classifications.")

# Collect all filenames
files = sorted([f for f in os.listdir(SUMMARY_DIR) if f.endswith(".json")])

# Sidebar filter
selected_file = st.sidebar.selectbox("Choose a report", files)

# Load summaries and classifications
summary_path = os.path.join(SUMMARY_DIR, selected_file)
classified_path = os.path.join(CLASSIFIED_DIR, selected_file)

with open(summary_path, "r", encoding="utf-8") as f:
    summary_data = json.load(f)

with open(classified_path, "r", encoding="utf-8") as f:
    classified_data = json.load(f)

chunks = summary_data.get("chunks", [])
topics = classified_data.get("topics", [])  # assume format: [{"chunk_index": 0, "topics": [...]}, ...]

# Build topic lookup
# Try both possibilities depending on format
# Handle both possible data formats (list or dict with 'topics')
if isinstance(classified_data, list):
    topic_list = classified_data
elif isinstance(classified_data, dict) and "topics" in classified_data:
    topic_list = classified_data["topics"]
else:
    topic_list = []

# Build lookup
topic_lookup = {t["chunk_index"]: t.get("topics", []) for t in topic_list}


# Display each chunk
for i, text in enumerate(chunks):
    st.markdown(f"---")
    st.markdown(f"#### 📌 Summary {i + 1}")
    st.markdown(f"**Text:** {text}")

    tags = topic_lookup.get(i, [])
    if tags:
        for tag in tags:
            st.markdown(
                f'<span style="background-color:#E8F3FF;padding:5px;border-radius:4px;margin-right:5px;">🔖 {tag}</span>',
                unsafe_allow_html=True)
