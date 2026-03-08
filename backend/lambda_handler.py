"""
AWS Lambda Handler for Soochna Setu AI
Uses Mangum to adapt FastAPI for Lambda + API Gateway
"""
from mangum import Mangum
from main import app

# Lambda handler
handler = Mangum(app, lifespan="off")
