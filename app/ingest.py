from pathlib import Path
from pypdf import PdfReader


def extract_pdf(path: str) -> list[dict]:
    reader = PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append({"page": i, "text": text})
    return pages


def chunk_words(text: str, size: int = 300, overlap: int = 50) -> list[str]:
    words = text.split()
    step = size - overlap
    chunks = []
    for start in range(0, len(words), step):
        piece = words[start:start + size]
        if piece:
            chunks.append(" ".join(piece))
        if start + size >= len(words):
            break
    return chunks


def chunk_document(path: str) -> list[dict]:
    source = Path(path).name
    out = []
    for p in extract_pdf(path):
        for j, chunk in enumerate(chunk_words(p["text"])):
            out.append({
                "id": f"{source}-p{p['page']}-c{j}",
                "text": chunk,
                "metadata": {"source": source, "page": p["page"]},
            })
    return out