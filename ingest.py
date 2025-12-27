import os
import glob
import json
import hashlib
from typing import List, Tuple

from langchain_community.document_loaders import (
    TextLoader,
    UnstructuredMarkdownLoader,
    PyPDFLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# --------------------
# Configuration
# --------------------
DOCS_DIR = "docs"
DB_DIR = "chroma_db"
HASH_FILE = "ingested_files.json"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# --------------------
# Hash Utilities
# --------------------
def compute_file_hash(path: str) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_ingested_hashes() -> dict:
    if not os.path.exists(HASH_FILE):
        return {}
    with open(HASH_FILE, "r") as f:
        return json.load(f)


def save_ingested_hashes(hashes: dict):
    with open(HASH_FILE, "w") as f:
        json.dump(hashes, f, indent=2)


# --------------------
# Document Loading
# --------------------
def load_new_or_changed_documents() -> Tuple[List[Document], dict]:
    ingested_hashes = load_ingested_hashes()
    updated_hashes = ingested_hashes.copy()
    documents: List[Document] = []

    file_paths = (
        glob.glob(os.path.join(DOCS_DIR, "**/*.md"), recursive=True)
        + glob.glob(os.path.join(DOCS_DIR, "**/*.txt"), recursive=True)
        + glob.glob(os.path.join(DOCS_DIR, "**/*.pdf"), recursive=True)
    )

    for file_path in file_paths:
        file_hash = compute_file_hash(file_path)

        # Skip unchanged files
        if ingested_hashes.get(file_path) == file_hash:
            continue

        print(f"Loading new/updated file: {file_path}")

        if file_path.endswith(".md"):
            loader = UnstructuredMarkdownLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path)
        else:
            loader = PyPDFLoader(file_path)

        loaded_docs = loader.load()

        source_name = os.path.basename(file_path)

        for doc in loaded_docs:
            # Normalize metadata consistently
            doc.metadata = doc.metadata or {}
            doc.metadata["source"] = source_name

        documents.extend(loaded_docs)
        updated_hashes[file_path] = file_hash

    return documents, updated_hashes


# --------------------
# Chunking
# --------------------
def split_documents(documents: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(documents)


# --------------------
# Ingestion Pipeline
# --------------------
def ingest() -> str:
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
        return f"Created {DOCS_DIR}. Please upload documents."

    print("Checking for new or modified documents...")
    documents, updated_hashes = load_new_or_changed_documents()

    if not documents:
        return "No new or changed documents to ingest."

    print(f"Found {len(documents)} new/updated documents.")

    print("Splitting documents...")
    chunks = split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")

    print("Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    if os.path.exists(DB_DIR):
        print("Updating existing ChromaDB...")
        db = Chroma(
            persist_directory=DB_DIR,
            embedding_function=embeddings,
        )
        db.add_documents(chunks)
    else:
        print("Creating new ChromaDB...")
        Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=DB_DIR,
        )

    save_ingested_hashes(updated_hashes)

    print("Ingestion complete.")
    return f"Success! Ingested {len(documents)} documents ({len(chunks)} chunks)."


# --------------------
# CLI Entry Point
# --------------------
if __name__ == "__main__":
    print(ingest())
