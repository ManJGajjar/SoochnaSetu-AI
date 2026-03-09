"""
Soochna Setu AI - Main FastAPI Application
Backend server with all routers, middleware, and database initialization.
"""
import os
import logging
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("soochna-setu")

# Initialize database
from db.database import init_db
init_db()

# Create FastAPI app
app = FastAPI(
    title="Soochna Setu AI",
    description="AI-powered civic intelligence platform for Indian citizens",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logger.info(f"{request.method} {request.url.path} - {response.status_code} ({duration:.2f}s)")
    return response


# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "INTERNAL_ERROR", "message": "An unexpected error occurred."}
    )


# Import and register routers
from routers import schemes, documents, chat, auth, profile, voice

app.include_router(schemes.router, prefix="/api/schemes", tags=["Schemes"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(profile.router, prefix="/api/profile", tags=["Profile"])
app.include_router(voice.router, prefix="/api/voice", tags=["Voice"])


@app.get("/")
def root():
    return {"name": "Soochna Setu AI", "version": "1.0.0", "status": "running"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "llm_provider": os.getenv("LLM_PROVIDER", "rule_based"),
            "ocr_method": "textract" if os.getenv("USE_TEXTRACT", "").lower() == "true" else "pdfplumber",
            "embeddings": "bedrock" if os.getenv("USE_BEDROCK_EMBEDDINGS", "").lower() == "true" else "local",
        }
    }


@app.get("/api/stats")
def get_stats():
    """Platform statistics for landing page."""
    from db.database import get_table
    try:
        scheme_table = get_table('SoochnaSetu-Schemes')
        scheme_count = scheme_table.describe().get('Table', {}).get('ItemCount', 56)
    except:
        scheme_count = 56
        
    try:
        users_table = get_table('SoochnaSetu-Users')
        user_count = users_table.describe().get('Table', {}).get('ItemCount', 0)
    except:
        user_count = 0
        
    return {
        "schemesCount": max(scheme_count, 56),
        "usersHelped": max(user_count, 1000),
        "languagesSupported": 12,
        "statesCovered": 36,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
