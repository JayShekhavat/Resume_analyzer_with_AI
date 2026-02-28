import pdfplumber
import spacy
import os


nlp = spacy.load("en_core_web_sm")
resume = r"C:\Users\jaine\PycharmProjects\resume_analyzer_app\datas\jay_cv.pdf"

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.lower()

def clean_text(text):
    doc = nlp(text)
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

print("Resume Parser Successful Run")


# if __name__ == "__main__":
#     file_path = r"C:\Users\jaine\PycharmProjects\resume_analyzer_app\datas\jay_cv.pdf"
#     #file_path = r"C:\Users\jaine\PycharmProjects\resume_analyzer_app\datas\jay_cv.pdf"
#     raw = extract_text_from_pdf(file_path)
#     print("\nFirst 300 characters of raw text:\n")
#     print(raw[:300])
#
#     cleaned = clean_text(raw)
#     print("\n" + "=" * 80 + "\nCleaned version (first 300 chars):\n")
#     print(cleaned[:300])