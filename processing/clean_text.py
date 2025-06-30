# clean_text.py
import os
import json
import re

INPUT_FOLDER = "data/cleaned_texts"
OUTPUT_FOLDER = "data/cleaned_texts"  # overwrite or modify in-place


def clean_text(raw_text):
    # Remove common header/footer patterns
    text = re.sub(r'DIW\\s+Weekly\\s+Report.*?\\n', '', raw_text)
    text = re.sub(r'\\n\\s*Page \\d+\\s*\\n', '', text)
    text = re.sub(r'Legal and Editorial Details.*', '', text, flags=re.DOTALL)

    # Remove excessive newlines and whitespace
    text = re.sub(r'\\n{2,}', '\\n\\n', text)
    text = re.sub(r'[ \\t]{2,}', ' ', text)

    return text.strip()


def process_all_json():
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(".json"):
            input_path = os.path.join(INPUT_FOLDER, filename)
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            cleaned = clean_text(data["text"])
            data["cleaned_text"] = cleaned

            with open(input_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ Cleaned: {filename}")


if __name__ == "__main__":
    process_all_json()
