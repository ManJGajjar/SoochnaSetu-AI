"""Chat Router - RAG-based conversational Q&A."""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from services.rag_service import query_pipeline
from services.llm_service import generate

router = APIRouter()


class ChatMessage(BaseModel):
    message: str
    language: str = "en"
    sessionId: Optional[str] = None
    userProfileId: Optional[str] = None


@router.post("/message")
def chat_message(request: ChatMessage):
    """Process a chat message through RAG pipeline."""
    # Try RAG pipeline first
    result = query_pipeline(
        question=request.message,
        language=request.language,
        collection_name="schemes",
    )

    # If RAG didn't find good context, use direct LLM
    if result["confidence"] < 0.3:
        direct = generate(
            f"You are Soochna Setu AI, a civic assistant for Indian citizens. "
            f"Answer this question about Indian government schemes: {request.message}",
            max_tokens=800,
        )
        return {
            "response": direct,
            "confidence": 0.7,
            "sources": [],
            "suggestions": result.get("followUpQuestions", []),
        }

    return {
        "response": result["answer"],
        "confidence": result["confidence"],
        "sources": result["sources"],
        "suggestions": result.get("followUpQuestions", []),
    }
