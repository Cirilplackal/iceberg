import re


def clean_text(text: str):

    # NORMALIZE WINDOWS NEWLINES

    text = text.replace("\r\n", "\n")

    # REMOVE EXCESSIVE SPACES
    # BUT PRESERVE NEWLINES

    text = re.sub(r"[ \t]+", " ", text)

    # REMOVE TOO MANY NEWLINES

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def smart_chunk_text(text: str, chunk_size: int = 800, overlap: int = 150):

    cleaned_text = clean_text(text)

    paragraphs = cleaned_text.split("\n")

    chunks = []

    current_chunk = ""

    for paragraph in paragraphs:

        if not paragraph.strip():

            continue

        if len(current_chunk) + len(paragraph) < chunk_size:

            current_chunk += paragraph + "\n"

        else:

            chunks.append(current_chunk.strip())

            overlap_text = current_chunk[-overlap:]

            current_chunk = overlap_text + "\n" + paragraph

    if current_chunk:

        chunks.append(current_chunk.strip())

    print("\nTOTAL CHUNKS:")
    print(len(chunks))

    for i, chunk in enumerate(chunks[:5]):

        print("\n" + "=" * 50)

        print(f"CHUNK {i}")

        print("=" * 50)

        print(chunk[:500])

    return chunks
