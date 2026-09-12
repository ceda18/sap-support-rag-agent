import json
import os
from datetime import datetime, timezone

import pdfplumber
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector

from core.config import settings
from core.db import init_db_extension

# SUMMARY:
# This module loads and chunks the SAP PaPM PDF, stores the chunks as embeddings in
# pgvector (used for semantic search) and as plain JSON on disk (used by BM25 keyword
# search at runtime, since BM25 keeps the chunks in memory instead of in the database).


def load_and_chunk_pdf(file_path: str) -> list[Document]:
    """Load a PDF file and split its content into chunks."""

    # (1): Extract text page by page, keeping the page number for citations.
    documents = []
    with pdfplumber.open(file_path) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and text.strip():
                metadata = {"source": os.path.basename(file_path), "page": page_idx + 1}
                documents.append(Document(page_content=text, metadata=metadata))

    # (2): Split the pages into smaller chunks, preferring section boundaries.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=True,  # needed, otherwise the section pattern below is literal text
        separators=[
            r"\n(?=\d+(?:\.\d+)+\s)", # 1. section-level, e.g. "1.1.2 "
            r"\n\n", # 2. paragraph-level
            r"\n", # 3. line-level
            r"\. ", # 4. sentence-level ('.' escaped, a regex wildcard...)
            r" ", # 5. word-level
            r"", # 6. character-level
        ],
    )
    raw_chunks = text_splitter.split_documents(documents)

    # (3): Enrich the chunks with additional metadata.
    current_time = datetime.now(timezone.utc).isoformat()
    for idx, chunk in enumerate(raw_chunks):
        chunk.metadata["chunk_index"] = idx
        chunk.metadata["ingested_at"] = current_time

    return raw_chunks


def save_chunks_to_json(chunks: list[Document], file_path: str):
    """Save the chunks as JSON so the BM25 retriever can load them at startup."""
    data = [{"page_content": c.page_content, "metadata": c.metadata} for c in chunks]
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def ingest_to_pgvector(chunks: list[Document]):
    """Generate embeddings for the chunks and store them in pgvector."""
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
    )

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=settings.COLLECTION_NAME,
        connection=settings.connection_string,
        use_jsonb=True,
        pre_delete_collection=True,  # wipe the old collection so re-running never duplicates
    )
    vector_store.add_documents(chunks)


if __name__ == "__main__":
    print("Initializing database extension for pgvector...")
    init_db_extension()

    if not os.path.exists(settings.PDF_PATH):
        print(f"❌ Critical error: File does not exist at path {settings.PDF_PATH}!")
        raise SystemExit(1)

    print(f"✅ File {settings.PDF_PATH} found! Starting parsing...")
    doc_chunks = load_and_chunk_pdf(settings.PDF_PATH)
    print(f"✅ Finished parsing. Created {len(doc_chunks)} chunks.")

    save_chunks_to_json(doc_chunks, settings.CHUNKS_PATH)
    print(f"✅ Chunks saved to {settings.CHUNKS_PATH}")

    print("Inserting chunks into the database...")
    ingest_to_pgvector(doc_chunks)
    print("✅ Insertion completed successfully!")
