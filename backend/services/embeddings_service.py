"""
Embeddings Service - Vector storage and semantic search.
Primary: Bedrock Titan Embeddings | Fallback: sentence-transformers
Storage: ChromaDB (simulates OpenSearch)
"""
import os
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

USE_BEDROCK_EMBEDDINGS = os.getenv("USE_BEDROCK_EMBEDDINGS", "false").lower() == "true"
_chroma_client = None
_local_model = None


_memory_store = {}

def get_or_create_collection(name: str = "documents"):
    if name not in _memory_store:
        _memory_store[name] = {"ids": [], "documents": [], "metadatas": [], "embeddings": []}
    return _memory_store[name]

def embed_text(text: str) -> List[float]:
    """Generate embedding for text."""
    if USE_BEDROCK_EMBEDDINGS:
        return _bedrock_embed(text)
    return _local_embed(text)

def _bedrock_embed(text: str) -> List[float]:
    import boto3, json
    client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({"inputText": text})
    )
    result = json.loads(response["body"].read())
    return result["embedding"]


def _local_embed(text: str) -> List[float]:
    """Use sentence-transformers for local embeddings."""
    global _local_model
    try:
        if _local_model is None:
            from sentence_transformers import SentenceTransformer
            _local_model = SentenceTransformer("all-MiniLM-L6-v2")
        return _local_model.encode(text).tolist()
    except ImportError:
        # Fallback: simple hash-based pseudo-embedding
        import hashlib
        h = hashlib.sha256(text.encode()).hexdigest()
        return [int(h[i:i+2], 16) / 255.0 for i in range(0, 64, 2)]


def store_chunks(chunks: List[Dict], collection_name: str = "user_uploads"):
    """Store document chunks with embeddings in memory store."""
    collection = get_or_create_collection(collection_name)

    for c in chunks:
        collection["ids"].append(c["chunkId"])
        collection["documents"].append(c["text"])
        collection["metadatas"].append({
            "source": c.get("source", ""),
            "pageNumber": c.get("pageNumber", 1),
            "position": c.get("position", 0),
        })
        # Generate and store embedding directly
        collection["embeddings"].append(embed_text(c["text"]))
        
    logger.info(f"Stored {len(chunks)} chunks in collection '{collection_name}'")


def similarity_search(query: str, collection_name: str = "user_uploads", top_k: int = 5) -> List[Dict]:
    """Search for similar chunks."""
    try:
        collection = get_or_create_collection(collection_name)
        if not collection["embeddings"]:
            return []
            
        query_emb = embed_text(query)
        
        # Calculate dot product (simple similarity) natively
        similarities = []
        for i, doc_emb in enumerate(collection["embeddings"]):
            # Simple dot product assuming normalized vectors
            score = sum(a * b for a, b in zip(query_emb, doc_emb))
            similarities.append((score, i))
            
        # Top K
        similarities.sort(reverse=True, key=lambda x: x[0])
        top_results = similarities[:top_k]

        output = []
        for score, i in top_results:
            output.append({
                "text": collection["documents"][i],
                "source": collection["metadatas"][i].get("source", ""),
                "pageNumber": collection["metadatas"][i].get("pageNumber", 1),
                "confidence": max(0, min(1, score)),
                "chunkId": collection["ids"][i],
            })
        return output
    except Exception as e:
        logger.error(f"Similarity search failed: {e}")
        return []
