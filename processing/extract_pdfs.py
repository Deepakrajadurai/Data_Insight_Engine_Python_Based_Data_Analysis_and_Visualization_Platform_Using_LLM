# extract_pdfs.py
import os
import fitz  # PyMuPDF
import json

INPUT_FOLDER = "data/refined_data_manual"
OUTPUT_FOLDER = "data/cleaned_texts"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def process_all_pdfs():
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(INPUT_FOLDER, filename)
            text = extract_text_from_pdf(input_path)
            cleaned_text = text.strip().replace("\n", "\n\n")
            output_filename = filename.replace(".pdf", ".json")
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump({"filename": filename, "text": cleaned_text}, f, ensure_ascii=False, indent=2)
            print(f"✅ Extracted: {filename}")

if __name__ == "__main__":
    process_all_pdfs()
