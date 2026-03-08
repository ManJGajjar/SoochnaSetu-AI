# Soochna Setu AI — सूचना सेतु AI

AI-powered civic intelligence platform connecting Indian citizens to 50+ government schemes.

## Quick Start (Local Development)

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
# Server runs at http://localhost:8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# App runs at http://localhost:3000
```

> **Note:** The app works fully without AWS credentials using local fallbacks (rule-based AI, pdfplumber OCR, ChromaDB). Adding AWS credentials upgrades to Bedrock AI, Textract OCR, etc.

---

## AWS Deployment (Lambda)

### Prerequisites
- AWS CLI configured with credentials
- Docker installed and running

### Step 1: Fill in AWS Credentials
Edit `backend/.env`:
```
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here
AWS_REGION=ap-south-1
LLM_PROVIDER=bedrock
USE_TEXTRACT=true
USE_BEDROCK_EMBEDDINGS=true
USE_AWS_VOICE=true
```

### Step 2: Deploy Backend to Lambda
```bash
cd backend
bash deploy_lambda.sh
```
This script will:
1. Create ECR repository
2. Build & push Docker image
3. Create Lambda function with IAM roles
4. Set up Function URL with CORS
5. Print the API URL

### Step 3: Deploy Frontend
Update `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=https://your-lambda-url-from-step-2
```

Then deploy frontend (Vercel, Amplify, or S3+CloudFront):
```bash
cd frontend
npm run build
# Upload .next/out to S3 or deploy via Vercel
```

---

## AWS Services Used

| Service | Purpose | Fallback |
|---|---|---|
| **Bedrock** (Claude 3 Haiku) | AI responses, scheme explanations | Rule-based keyword matching |
| **Textract** | Document OCR | pdfplumber (local) |
| **S3** | Document storage | Local filesystem |
| **Transcribe** | Speech-to-text | Web Speech API (browser) |
| **Polly** | Text-to-speech | Web Speech Synthesis (browser) |
| **Lambda** | Backend hosting | Local uvicorn server |

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/schemes/` | GET | List all 50 schemes |
| `/api/schemes/match` | POST | Match schemes to user profile |
| `/api/schemes/{id}/apply-guide` | GET | Step-by-step application guide |
| `/api/documents/upload` | POST | Upload & OCR a document |
| `/api/documents/{id}/ask` | POST | RAG Q&A on document |
| `/api/chat/message` | POST | AI chatbot |
| `/api/auth/register` | POST | Register with OTP |
| `/api/profile/` | POST/GET/PUT | User profile CRUD |
| `/api/voice/transcribe` | POST | Speech-to-text |
| `/health` | GET | Service health check |

## Tech Stack
- **Backend:** Python, FastAPI, SQLite, Mangum (Lambda)
- **Frontend:** Next.js, React, TypeScript, Tailwind CSS
- **AI:** AWS Bedrock, ChromaDB, sentence-transformers
- **OCR:** AWS Textract, pdfplumber

## Team: THE CHOSEN ONES
