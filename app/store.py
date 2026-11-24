import chromadb
from fastembed import TextEmbedding

EMBED_MODEL = "BAAI/bge-small-en-v1.5"

_embedder = None
_collection = None



def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = TextEmbedding(EMBED_MODEL)
    return _embedder


def get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path="chroma_db")
        _collection = client.get_or_create_collection(
            name="docs",
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def add_chunks(chunks: list[dict]) -> int:
    if not chunks:
        return 0
    texts = [c["text"] for c in chunks]
    vectors = [v.tolist() for v in get_embedder().passage_embed(texts)]
    get_collection().upsert(
        ids=[c["id"] for c in chunks],
        embeddings=vectors,
        documents=texts,
        metadatas=[c["metadata"] for c in chunks],
    )
    return len(chunks)


def remove_source(source: str) -> None:
    get_collection().delete(where={"source": source})


def search(question: str, k: int = 5) -> list[dict]:
    vector = next(iter(get_embedder().query_embed(question))).tolist()
    res = get_collection().query(
        query_embeddings=[vector],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    hits = []
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        hits.append({
            "text": doc,
            "source": meta["source"],
            "page": meta["page"],
            "score": round(1 - dist, 3),
        })
    return hits