"""
RAG Service - Retrieval-Augmented Generation pipeline.
Retrieves relevant chunks → builds context prompt → calls LLM → validates citations.
"""
import logging
from typing import Dict, List, Any, Optional
from services.llm_service import generate
from services.embeddings_service import similarity_search

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are Soochna Setu AI, a helpful civic assistant for Indian citizens. "
    "Always cite your sources. If unsure, say so. "
    "Simplify complex language to grade-5 reading level. "
    "Answer in the language the user asks in."
)


def query_pipeline(
    question: str,
    user_profile: Optional[Dict] = None,
    collection_name: str = "user_uploads",
    language: str = "en",
) -> Dict[str, Any]:
    """Full RAG pipeline: embed → retrieve → generate → validate."""
    # Step 1: Retrieve relevant chunks
    chunks = similarity_search(question, collection_name=collection_name, top_k=5)

    # Step 2: Build context
    context_parts = []
    sources = []
    for i, chunk in enumerate(chunks):
        context_parts.append(f"[Source {i+1}, Page {chunk.get('pageNumber', '?')}]: {chunk['text'][:500]}")
        sources.append({
            "documentId": chunk.get("source", "unknown"),
            "documentName": chunk.get("source", "Document"),
            "pageNumber": chunk.get("pageNumber", 1),
            "chunkId": chunk.get("chunkId", ""),
            "excerpt": chunk["text"][:200],
            "confidence": chunk.get("confidence", 0.8),
        })

    context = "\n\n".join(context_parts) if context_parts else "No specific document context available."

    # Step 3: Build prompt
    profile_context = ""
    if user_profile:
        profile_context = (
            f"\nUser Profile: Age {user_profile.get('age', 'unknown')}, "
            f"Occupation: {user_profile.get('occupation', 'unknown')}, "
            f"State: {user_profile.get('state', 'unknown')}, "
            f"Income: {user_profile.get('incomeBracket', 'unknown')}"
        )

    prompt = f"""{SYSTEM_PROMPT}

Context from documents:
{context}
{profile_context}

User Question: {question}

Instructions: Answer the question based on the context above. Cite sources with [Source X, Page Y].
If the context doesn't contain enough information, say so clearly.
Add a "What This Means For You" section if user profile is available.
Language: {'Hindi' if language == 'hi' else 'English'}"""

    # Step 4: Generate response
    answer = generate(prompt, max_tokens=1000, temperature=0.3)

    # Step 5: Calculate confidence
    confidence = 0.5
    if chunks:
        avg_chunk_confidence = sum(c.get("confidence", 0.5) for c in chunks) / len(chunks)
        confidence = min(0.95, avg_chunk_confidence)

    # Add disclaimer if low confidence
    if confidence < 0.7:
        answer = (
            "⚠ This answer is based on limited information. "
            "Please verify with official sources.\n\n" + answer
        )

    # Step 6: Generate follow-up questions
    follow_ups = _generate_follow_ups(question)

    return {
        "answer": answer,
        "sources": sources,
        "confidence": round(confidence, 2),
        "followUpQuestions": follow_ups,
    }


def generate_summary(text: str, language: str = "en") -> str:
    """Generate a plain-language summary of document text."""
    prompt = f"""{SYSTEM_PROMPT}

Summarize the following government document in simple, grade-5 reading level language.
Use bullet points for key points.
Language: {'Hindi' if language == 'hi' else 'English'}

Document text (first 3000 chars):
{text[:3000]}

Provide:
1. A 3-sentence summary
2. Key points as bullet list
3. Important numbers/statistics mentioned"""

    return generate(prompt, max_tokens=800)


def _generate_follow_ups(question: str) -> List[str]:
    """Generate follow-up question suggestions."""
    q = question.lower()
    if "kisan" in q or "farmer" in q:
        return ["How do I apply for PM-KISAN?", "What documents do I need?", "When is the next installment?"]
    if "ayushman" in q or "health" in q:
        return ["Which hospitals are covered?", "How to get Ayushman card?", "What treatments are covered?"]
    if "scholarship" in q or "student" in q:
        return ["What is the scholarship amount?", "When is the deadline?", "What documents are needed?"]
    return ["What schemes am I eligible for?", "How do I apply?", "What documents do I need?"]
