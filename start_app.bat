@echo off
echo 🔄 Creating virtual environment...
python -m venv venv

echo ✅ Activating virtual environment...
call venv\Scripts\activate

echo 📦 Installing requirements...
pip install --upgrade pip
pip install streamlit pandas matplotlib scikit-learn sentence-transformers PyMuPDF langchain openai chromadb networkx plotly sompy gtts

echo 🚀 Launching Streamlit App...
streamlit run app/main.py

pause
