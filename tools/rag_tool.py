"""
Inner RAG retrieval tool for Tripsaarthi's multi-agent system.
Uses Hugging Face's hosted Inference API for embeddings — free, and the
model runs remotely so it doesn't consume Render's memory.
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

from langchain_core.tools import tool
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_pinecone import PineconeVectorStore

PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
HF_TOKEN = os.environ["HF_TOKEN"]
INDEX_NAME = os.environ.get("RAG_INDEX", "tripsaarthi-policies-free")

# Must match rag_ingest.py's model exactly.
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# BGE cosine scores for relevant matches tend to run lower than OpenAI's —
# tune this against real queries once deployed.
SIMILARITY_THRESHOLD = 0.55

_embeddings = HuggingFaceInferenceAPIEmbeddings(api_key=HF_TOKEN, model_name=EMBEDDING_MODEL)
_store = PineconeVectorStore(index_name=INDEX_NAME, embedding=_embeddings, pinecone_api_key=PINECONE_API_KEY)

_reranker = None
if os.environ.get("COHERE_API_KEY"):
    import cohere
    _cohere_client = cohere.Client(os.environ["COHERE_API_KEY"])

    def _rerank(query: str, docs: list, top_n: int = 5):
        if not docs:
            return docs
        result = _cohere_client.rerank(
            model="rerank-v3.5",
            query=query,
            documents=[d.page_content for d in docs],
            top_n=min(top_n, len(docs)),
        )
        return [docs[r.index] for r in result.results]

    _reranker = _rerank


@tool
def search_knowledge_base(query: str, doc_type: Optional[str] = None) -> str:
    """
    Search Tripsaarthi's internal knowledge base (company policies, SOPs,
    refund/cancellation rules, FAQs). Use this whenever the user asks about
    company policy, procedures, or anything that would live in internal docs
    (e.g. "what's our cancellation policy", "how do refunds work").

    Args:
        query: The user's question, in natural language.
        doc_type: Optional filter, e.g. "refund_policy", "faq".
    """
    filter_dict = {"doc_type": doc_type} if doc_type else None

    try:
        results = _store.similarity_search_with_score(query, k=20, filter=filter_dict)
    except Exception as e:
        # HF's free Inference API occasionally cold-starts or rate-limits —
        # surface a clean message instead of crashing the whole agent turn.
        return f"Knowledge base search temporarily unavailable: {e}"

    relevant = [(doc, score) for doc, score in results if score >= SIMILARITY_THRESHOLD]

    if not relevant:
        return "No relevant information found in the knowledge base for this query."

    docs = [doc for doc, _ in relevant]
    top_docs = _reranker(query, docs, top_n=5) if _reranker else docs[:5]

    formatted = []
    for d in top_docs:
        source = d.metadata.get("source", "unknown")
        formatted.append(f"[Source: {source}]\n{d.page_content}")

    return "\n\n---\n\n".join(formatted)