from langchain_core.documents import Document
import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector
from datetime import datetime, timezone
import os
from app.core.db import CONNECTION_STRING, init_db_extension

# SUMMARY:
# This module provides functions to load and chunk PDF documents, generate embeddings for the chunks, and store them in a PostgreSQL database using the pgvector extension.

def load_and_chunk_pdf(file_path: str) -> list[Document]:
    """Load a PDF file and split its content into chunks."""

    # (1): Load the PDF and extract text from each page, creating Document objects with metadata.
    documents = []
    with pdfplumber.open(file_path) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and text.strip():  # Check if the text is not empty
                # Split the text into chunks of 1000 characters
                metadata = {
                    "source": os.path.basename(file_path),
                    "page": page_idx + 1
                }
                documents.append(Document(page_content=text, metadata=metadata))

        # (2): Use RecursiveCharacterTextSplitter to further split the documents into smaller chunks.
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators = [
                "\n(?=\d+(?:\.\d+)+\s)", # 1. section-level, e.g., "1.1.2 "
                "\n\n", # 2. paragraph-level
                "\n", # 3. line-level
                ". ", # 4. sentence-level
                " ", # 5. word-level
                "" # 6. charater-level
            ]
        )

        raw_chunks = text_splitter.split_documents(documents)

        # (3): Enrich the chunks with additional metadata, such as the current timestamp.
        current_time = datetime.now(timezone.utc).isoformat()
        enriched_chunks = []
        for idx, chunk in enumerate(raw_chunks):
            chunk.metadata["chunk_index"] = idx
            chunk.metadata["ingested_at"] = current_time
            enriched_chunks.append(chunk)

    return enriched_chunks


def ingest_to_pgvector(chunks: list[Document]):
    """Generate embeddings for the document chunks and store them in a PostgreSQL database using pgvector."""

    # (1): Initialize the HuggingFaceEmbeddings model to generate embeddings for the document chunks.
    embeddings = HuggingFaceEmbeddings(
        model_name=os.environ.get("EMBEDDING_MODEL_NAME"),
        model_kwargs={'device': 'cpu'}
    )

    # (2): Create a PGVector instance to handle the storage of embeddings in the PostgreSQL database.
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name="sap_rag_collection",
        connection=CONNECTION_STRING,
        use_jsonb=True,
    )
    vector_store.add_documents(chunks)

if __name__ == "__main__":
    PDF_PATH = "/app/data/Application_Help_for_SAP_PaPM.pdf"
    
    print("Initializing database extension for pgvector...")
    init_db_extension()
    
    if os.path.exists(PDF_PATH):
        print(f"✅File {PDF_PATH} found! Starting parsing...")
        doc_chunks = load_and_chunk_pdf(PDF_PATH)
        print(f"✅ Finished parsing. Inserting {len(doc_chunks)} chunks into the database...")
        ingest_to_pgvector(doc_chunks)
        print("✅ Insertion completed successfully!")
    else:
        print(f"❌ Critical error: File does not exist at path {PDF_PATH} within the container!")


