from pathlib import Path
import re

RAW_DIR = Path("ichat_ai/dataset/raw")
CLEAN_DIR = Path("ichat_ai/dataset/cleaned")

def clean_text(text):
    text = text.replace("\x00", "")
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def import_text_file(filename):
    source = RAW_DIR / filename

    if not source.exists():
        print("File nahi mili:", source)
        return

    text = source.read_text(encoding="utf-8")
    cleaned = clean_text(text)

    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    destination = CLEAN_DIR / filename
    destination.write_text(cleaned, encoding="utf-8")

    print("Text import complete.")
    print("Original:", source)
    print("Cleaned :", destination)
    print("Characters:", len(cleaned))

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Use: python -m ichat_ai.learning.import_text filename.txt")
    else:
        import_text_file(sys.argv[1])
