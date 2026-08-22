"""
Inner RAG ingestion pipeline for Tripsaarthi (Hugging Face Inference API embeddings).

Uses Hugging Face's hosted Inference API — the embedding model runs on HF's
servers, not on Render. This avoids both problems we hit before:
  - No per-token cost (free, with fair-use rate limits)
  - No local model loading, so no memory crash on Render's free tier

Usage:
    python scripts/rag_ingest.py --source-dir ./knowledge_base

Requirements:
    pip install langchain langchain-community langchain-pinecone \
                pinecone-client python-dotenv huggingface_hub \
                unstructured pypdf python-docx
"""

import argparse
import hashlib
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    TextLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

# ---- Config -----------------------------------------------------------

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"  # runs remotely on HF's servers, not locally
HF_TOKEN = os.environ["HF_TOKEN"]
CHUNK_SIZE = 700
CHUNK_OVERLAP = 120
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
PINECONE_CLOUD = os.environ.get("PINECONE_CLOUD", "aws")
PINECONE_REGION = os.environ.get("PINECONE_REGION", "us-east-1")

# New index — different from the OpenAI one and the local-HF one, since
# each embedding model produces a different vector space/dimension.
INDEX_NAME_DEFAULT = "tripsaarthi-policies-hf-api"

LOADER_MAP = {
    ".pdf": PyPDFLoader,
    ".docx": UnstructuredWordDocumentLoader,
    ".txt": TextLoader,
    ".md": TextLoader,
}


def chunk_hash(source: str, content: str) -> str:
    return hashlib.sha256(f"{source}::{content}".encode("utf-8")).hexdigest()


def load_documents(source_dir: str):
    docs = []
    for path in Path(source_dir).rglob("*"):
        if path.suffix.lower() not in LOADER_MAP:
            continue
        loader_cls = LOADER_MAP[path.suffix.lower()]
        loaded = loader_cls(str(path)).load()
        for d in loaded:
            d.metadata["source"] = str(path)
            d.metadata["doc_type"] = path.parent.name
        docs.extend(loaded)
    return docs


def get_existing_ids(pc: Pinecone, index_name: str, namespace: str = "") -> set:
    if index_name not in [i.name for i in pc.list_indexes()]:
        return set()
    index = pc.Index(index_name)
    existing = set()
    for id_batch in index.list(namespace=namespace):
        existing.update(id_batch)
    return existing


def ensure_index(pc: Pinecone, index_name: str, dimension: int):
    if index_name not in [i.name for i in pc.list_indexes()]:
        print(f"Creating Pinecone index '{index_name}' (dimension={dimension}) ...")
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_REGION),
        )


def main(source_dir: str, index_name: str):
    print(f"Loading documents from {source_dir} ...")
    raw_docs = load_documents(source_dir)
    print(f"Loaded {len(raw_docs)} source documents.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(raw_docs)
    print(f"Split into {len(chunks)} chunks.")

    print(f"Using Hugging Face Inference API for embeddings ({EMBEDDING_MODEL}) — remote, no local download.")
    embeddings = HuggingFaceInferenceAPIEmbeddings(api_key=HF_TOKEN, model_name=EMBEDDING_MODEL)

    pc = Pinecone(api_key=PINECONE_API_KEY)
    vector_size = len(embeddings.embed_query("dimension probe"))
    ensure_index(pc, index_name, vector_size)

    existing_ids = get_existing_ids(pc, index_name)

    to_upsert = []
    for c in chunks:
        cid = chunk_hash(c.metadata.get("source", ""), c.page_content)
        c.metadata["chunk_id"] = cid
        if cid not in existing_ids:
            to_upsert.append(c)

    print(f"{len(to_upsert)} new/changed chunks to embed (skipping {len(chunks) - len(to_upsert)} unchanged).")

    if not to_upsert:
        print("Nothing to do — knowledge base is up to date.")
        return

    store = PineconeVectorStore(index_name=index_name, embedding=embeddings, pinecone_api_key=PINECONE_API_KEY)
    ids = [c.metadata["chunk_id"] for c in to_upsert]

    # Smaller batches here — the free Inference API can be slow/rate-limited
    # under load, so keep batches modest and let it breathe between calls.
    batch_size = 20
    for i in range(0, len(to_upsert), batch_size):
        batch_docs = to_upsert[i:i + batch_size]
        batch_ids = ids[i:i + batch_size]
        store.add_documents(batch_docs, ids=batch_ids)
        print(f"  upserted {min(i + batch_size, len(to_upsert))}/{len(to_upsert)}")

    print(f"Done. Upserted {len(to_upsert)} chunks into index '{index_name}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--index", default=INDEX_NAME_DEFAULT)
    args = parser.parse_args()
    main(args.source_dir, args.index)