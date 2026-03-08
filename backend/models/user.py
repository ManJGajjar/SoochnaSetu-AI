from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class UserProfile(BaseModel):
    userId: Optional[str] = None
    age: int
    incomeBracket: str  # "BPL" | "0-2.5L" | "2.5-5L" | "5-10L" | "10L+"
    occupation: str
    state: str
    district: Optional[str] = None
    category: str  # "General" | "SC" | "ST" | "OBC"
    disability: bool = False
    disabilityType: Optional[str] = None
    gender: Optional[str] = None
    language: str = "en"
    phone: Optional[str] = None
    name: Optional[str] = None
    needs: List[str] = []
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None


class UserProfileCreate(BaseModel):
    age: int
    incomeBracket: str
    occupation: str
    state: str
    district: Optional[str] = None
    category: str = "General"
    disability: bool = False
    disabilityType: Optional[str] = None
    gender: Optional[str] = None
    language: str = "en"
    phone: Optional[str] = None
    name: Optional[str] = None
    needs: List[str] = []


class AuthRegister(BaseModel):
    phone: str
    name: str
    language: str = "en"


class AuthVerifyOTP(BaseModel):
    phone: str
    otp: str


class AuthLogin(BaseModel):
    phone: str
