import fitz  # this is pymupdf
import sys
import os

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    
    for page in document:
        text += page.get_text()

    return text

def save_text_to_file(pdf_path, text):
    txt_path = os.path.splitext(pdf_path)[0] + ".txt"
    
    with open(txt_path, 'w') as f:
        f.write(text)
    
    print(f"Text saved to {txt_path}")

# Check if video ID is provided as a command line argument
if len(sys.argv) < 2:
    print("Please provide the PDF file path as a command line argument.")
    print("Example usage: python script_name.py </path/to/pdf>")
else:
    pdf_path = sys.argv[1]
    text = extract_text_from_pdf(pdf_path)
    save_text_to_file(pdf_path, text)

