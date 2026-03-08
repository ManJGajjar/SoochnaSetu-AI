"""
OCR Service - Document text extraction.
Primary: AWS Textract | Fallback: pdfplumber + PyMuPDF
"""
import os
import json
import logging
import uuid
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

USE_TEXTRACT = os.getenv("USE_TEXTRACT", "false").lower() == "true"


def extract_text_from_pdf(file_bytes: bytes, filename: str = "") -> Dict[str, Any]:
    """Extract text from PDF using Textract or local libraries."""
    if USE_TEXTRACT:
        try:
            return _extract_with_textract(file_bytes)
        except Exception as e:
            logger.warning(f"Textract failed: {e}, falling back to local extraction")

    return _extract_locally(file_bytes, filename)


def _extract_with_textract(file_bytes: bytes) -> Dict[str, Any]:
    """Use AWS Textract for OCR."""
    import boto3
    client = boto3.client("textract", region_name=os.getenv("AWS_REGION", "us-east-1"))

    response = client.detect_document_text(Document={"Bytes": file_bytes})

    pages_text = {}
    for block in response.get("Blocks", []):
        if block["BlockType"] == "LINE":
            page = block.get("Page", 1)
            if page not in pages_text:
                pages_text[page] = []
            pages_text[page].append(block["Text"])

    pages = [{"page": p, "text": "\n".join(lines)} for p, lines in sorted(pages_text.items())]
    full_text = "\n\n".join([p["text"] for p in pages])
    chunks = chunk_text(full_text, filename)

    return {
        "pages": pages,
        "chunks": chunks,
        "metadata": {
            "page_count": len(pages),
            "word_count": len(full_text.split()),
            "extraction_confidence": 0.95,
            "method": "textract",
        }
    }


def _extract_locally(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    """Use pdfplumber for local text extraction."""
    import io
    pages = []
    full_text = ""

    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                text = page.extract_text() or ""
                pages.append({"page": i, "text": text})
                full_text += text + "\n\n"
    except ImportError:
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for i, page in enumerate(doc, 1):
                text = page.get_text()
                pages.append({"page": i, "text": text})
                full_text += text + "\n\n"
            doc.close()
        except ImportError:
            logger.error("No PDF library available. Install pdfplumber or PyMuPDF.")
            pages = [{"page": 1, "text": f"[PDF content from {filename}]"}]
            full_text = f"Document: {filename}"

    chunks = chunk_text(full_text, filename)

    return {
        "pages": pages,
        "chunks": chunks,
        "metadata": {
            "page_count": len(pages),
            "word_count": len(full_text.split()),
            "extraction_confidence": 0.85,
            "method": "pdfplumber",
        }
    }


def chunk_text(text: str, source: str = "", chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
    """Split text into overlapping chunks for embedding."""
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk_words = words[i: i + chunk_size]
        if not chunk_words:
            break

        chunk_text_str = " ".join(chunk_words)
        page_estimate = max(1, (i // 250) + 1)

        chunks.append({
            "chunkId": str(uuid.uuid4())[:8],
            "text": chunk_text_str,
            "source": source,
            "pageNumber": page_estimate,
            "position": len(chunks),
            "wordCount": len(chunk_words),
        })

    return chunks
