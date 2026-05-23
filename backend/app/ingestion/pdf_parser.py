import fitz


def extract_text_from_pdf(file_path: str):

    document = fitz.open(file_path)

    full_text = ""

    for page in document:

        full_text += page.get_text()

    return full_text