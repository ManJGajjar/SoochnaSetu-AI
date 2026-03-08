"""Auth Router - JWT-based auth simulating Cognito."""
import uuid
import os
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY", "soochna-setu-secret-key-2024")

# In-memory OTP store (would be Cognito in production)
_otps = {}


class RegisterRequest(BaseModel):
    phone: str
    name: str
    language: str = "en"


class VerifyOTPRequest(BaseModel):
    phone: str
    otp: str


class LoginRequest(BaseModel):
    phone: str


def _create_token(user_id: str) -> str:
    """Create a simple JWT token."""
    try:
        from jose import jwt
        payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(days=7),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    except ImportError:
        import hashlib
        return hashlib.sha256(f"{user_id}{SECRET_KEY}".encode()).hexdigest()


@router.post("/register")
def register(request: RegisterRequest):
    """Register a new user and send OTP."""
    user_id = str(uuid.uuid4())[:12]
    _otps[request.phone] = {"otp": "1234", "user_id": user_id, "name": request.name}
    return {
        "userId": user_id,
        "message": "OTP sent to your phone (demo: use 1234)",
        "sessionToken": _create_token(user_id),
    }


@router.post("/verify-otp")
def verify_otp(request: VerifyOTPRequest):
    """Verify OTP and return access token."""
    stored = _otps.get(request.phone)
    if not stored:
        raise HTTPException(400, "No OTP sent to this number. Please register first.")

    if request.otp != stored["otp"] and request.otp != "1234":
        raise HTTPException(400, "Invalid OTP")

    token = _create_token(stored["user_id"])
    return {
        "accessToken": token,
        "userId": stored["user_id"],
        "expiresIn": 604800,
    }


@router.post("/login")
def login(request: LoginRequest):
    """Send OTP for login."""
    _otps[request.phone] = {"otp": "1234", "user_id": str(uuid.uuid4())[:12]}
    return {"message": "OTP sent (demo: use 1234)"}
