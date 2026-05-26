import re

import fitz


def clean_extracted_text(text: str):

    # REMOVE EXCESSIVE WHITESPACE

    text = re.sub(r"\s+", " ", text)

    # REMOVE PAGE NUMBER LINES

    text = re.sub(r"\b\d+\b", "", text)

    # REMOVE COMMON FOOTER PATTERNS

    footer_patterns = [r"To find out more.*?", r"www\..*?", r"email .*?", r"policy@.*?"]

    for pattern in footer_patterns:

        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    return text.strip()


def extract_text_from_pdf(file_path: str):

    document = fitz.open(file_path)

    full_text = ""

    for page in document:

        text = page.get_text()

        cleaned = clean_extracted_text(text)

        full_text += cleaned + "\n"

    return full_text
