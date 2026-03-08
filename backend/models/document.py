from pydantic import BaseModel
from typing import Optional, List


class Citation(BaseModel):
    documentId: str
    documentName: str
    pageNumber: int
    chunkId: str
    excerpt: str
    confidence: float


class DocumentMetadata(BaseModel):
    documentId: str
    userId: Optional[str] = None
    fileName: str
    fileSize: int = 0
    fileType: str = ""
    s3Key: Optional[str] = None
    uploadedAt: Optional[str] = None
    processingStatus: str = "pending"
    processingProgress: int = 0
    pageCount: Optional[int] = None
    extractedText: Optional[bool] = None
    embeddingsGenerated: Optional[bool] = None
    error: Optional[str] = None


class DocumentUploadResponse(BaseModel):
    documentId: str
    fileName: str
    status: str
    pageCount: Optional[int] = None
    summary: Optional[str] = None


class DocumentExplainRequest(BaseModel):
    query: str
    language: str = "en"
    simplificationLevel: int = 5


class ExplanationResponse(BaseModel):
    explanation: str
    citations: List[Citation] = []
    confidence: float = 0.0
    keyPoints: List[str] = []
    whatThisMeansForYou: Optional[str] = None
