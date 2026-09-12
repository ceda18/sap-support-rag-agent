import json

from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector

from core.config import settings

# SUMMARY:
# Builds a hybrid retriever: BM25 for keyword matches, pgvector for semantic
# matches, combined by EnsembleRetriever. BM25 needs the chunks in memory, so
# it loads them from the JSON file produced by ingest.py.


def load_chunks_from_json(file_path: str) -> list[Document]:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Document(page_content=d["page_content"], metadata=d["metadata"]) for d in data]


def build_retriever() -> EnsembleRetriever:
    
    # Keyword search (BM25)
    chunks = load_chunks_from_json(settings.CHUNKS_PATH)
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = settings.TOP_K

    # Semantic search (pgvector)
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
    )
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=settings.COLLECTION_NAME,
        connection=settings.connection_string,
        use_jsonb=True,
    )
    vector_retriever = vector_store.as_retriever(search_kwargs={"k": settings.TOP_K})

    return EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[settings.BM25_WEIGHT, settings.VECTOR_WEIGHT],
    )


def format_docs(docs: list[Document]) -> str:
    """Render retrieved chunks into a single context block, tagged with page numbers for citation."""
    parts = []
    for d in docs:
        page = d.metadata.get("page", "?")
        source = d.metadata.get("source", "unknown")
        parts.append(f"[source: {source} | p. {page}]\n{d.page_content.strip()}")
    return "\n\n---\n\n".join(parts)