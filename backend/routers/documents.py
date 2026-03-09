"""Documents Router - Upload, OCR processing, summary, Q&A."""
import uuid
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.ocr_service import extract_text_from_pdf
from services.embeddings_service import store_chunks
from services.rag_service import query_pipeline, generate_summary

router = APIRouter()

from db.database import get_table


class AskRequest(BaseModel):
    query: str
    language: str = "en"


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document through OCR pipeline."""
    if not file.filename:
        raise HTTPException(400, "No file provided")

    allowed = (".pdf", ".png", ".jpg", ".jpeg")
    ext = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in allowed:
        raise HTTPException(400, f"Unsupported file type. Allowed: {', '.join(allowed)}")

    contents = await file.read()
    if len(contents) > 50 * 1024 * 1024:
        raise HTTPException(413, "File size exceeds maximum allowed size of 50MB")

    doc_id = str(uuid.uuid4())[:12]

    # Process document
    try:
        result = extract_text_from_pdf(contents, file.filename)
    except Exception as e:
        raise HTTPException(500, f"Document processing failed: {str(e)}")

    # Store chunks in vector store
    chunks = result.get("chunks", [])
    if chunks:
        for c in chunks:
            c["source"] = file.filename
        try:
            store_chunks(chunks, collection_name=f"doc_{doc_id}")
        except Exception:
            pass  # Vector store optional

    # Generate summary
    full_text = "\n".join([p.get("text", "") for p in result.get("pages", [])])
    summary = generate_summary(full_text[:3000]) if full_text else "No text extracted."

    # Store metadata in DynamoDB
    table = get_table('SoochnaSetu-Documents')
    doc_item = {
        "documentId": doc_id,
        "fileName": file.filename,
        "uploadedAt": datetime.utcnow().isoformat(),
        "status": "completed",
        "pageCount": result["metadata"]["page_count"],
        "wordCount": result["metadata"]["word_count"],
        "summary": summary,
        "fullText": full_text,
    }
    table.put_item(Item=doc_item)

    return {
        "documentId": doc_id,
        "fileName": file.filename,
        "status": "completed",
        "pageCount": result["metadata"]["page_count"],
        "wordCount": result["metadata"]["word_count"],
        "summary": summary,
        "extractionMethod": result["metadata"]["method"],
        "confidence": result["metadata"]["extraction_confidence"],
    }


@router.get("/{doc_id}/summary")
def get_summary(doc_id: str):
    """Get AI-generated summary for a processed document."""
    table = get_table('SoochnaSetu-Documents')
    response = table.get_item(Key={'documentId': doc_id})
    doc = response.get('Item')
    
    if not doc:
        raise HTTPException(404, f"Document {doc_id} not found")

    return {
        "documentId": doc_id,
        "summary": doc.get("summary", ""),
        "pageCount": doc.get("pageCount", 0),
        "wordCount": doc.get("wordCount", 0),
    }


@router.post("/{doc_id}/ask")
def ask_document(doc_id: str, request: AskRequest):
    """RAG Q&A on a specific document."""
    table = get_table('SoochnaSetu-Documents')
    response = table.get_item(Key={'documentId': doc_id})
    doc = response.get('Item')
    
    if not doc:
        raise HTTPException(404, f"Document {doc_id} not found")

    result = query_pipeline(
        question=request.query,
        collection_name=f"doc_{doc_id}",
        language=request.language,
    )

    return {
        "documentId": doc_id,
        "question": request.query,
        "answer": result["answer"],
        "sources": result["sources"],
        "confidence": result["confidence"],
        "followUpQuestions": result.get("followUpQuestions", []),
    }
