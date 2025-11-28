from typing import List
from pypdf import PdfReader
import math

def extract_text_chunks(pdf_path: str, chunk_size: int = 800) -> List[str]:
    """
    Extract text from PDF and split in roughly chunk_size tokens (characters here).
    """
    reader = PdfReader(pdf_path)
    full_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text.append(text)
    text = "\n\n".join(full_text)
    # naive chunking by characters - replace with token-aware chunker if needed
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i: i + chunk_size])
    return chunks
