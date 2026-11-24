from pathlib import Path
from app.ingest import chunk_document
from app.store import add_chunks, remove_source, search

for pdf in sorted(Path("sample_docs").glob("*.pdf")):
    remove_source(pdf.name)
    n = add_chunks(chunk_document(str(pdf)))
    print(f"{pdf.name}: {n} chunks stored")

questions = [
    "How many days of annual leave do I get?",
    "How long do I have to return a product?",
    "Does the camera work on 5GHz wifi?",
    "Does Lumora offer a 401(k) match?",
]

for q in questions:
    print("\nQ:", q)
    for hit in search(q, k=3):
        print(f"  {hit['score']}  {hit['source']} p{hit['page']}: {hit['text'][:90]}...")