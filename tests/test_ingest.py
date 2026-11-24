from app.ingest import chunk_document

chunks = chunk_document("sample_docs\Lumora_Employee_Handbook.pdf")
print(len(chunks), "chunks")
print(chunks[0])
print(chunks[1]["text"][:200])