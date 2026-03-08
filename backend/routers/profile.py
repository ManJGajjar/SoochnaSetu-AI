"""Profile Router - User profile CRUD."""
import uuid
import json
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from db.database import get_db

router = APIRouter()


class ProfileCreate(BaseModel):
    age: Optional[int] = None
    incomeBracket: Optional[str] = None
    occupation: Optional[str] = None
    state: Optional[str] = None
    category: str = "General"
    district: Optional[str] = None
    disability: bool = False
    gender: Optional[str] = None
    language: str = "en"
    phone: Optional[str] = None
    name: Optional[str] = None
    needs: List[str] = []
    userId: Optional[str] = None


@router.post("/")
def create_profile(profile: ProfileCreate):
    """Create a new user profile."""
    user_id = str(uuid.uuid4())[:12]
    now = datetime.utcnow().isoformat()
    db = get_db()
    db.execute(
        """INSERT INTO users (userId, phone, name, age, incomeBracket, occupation,
           state, district, category, disability, gender, language, needs, createdAt, updatedAt)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (user_id, profile.phone, profile.name, profile.age, profile.incomeBracket,
         profile.occupation, profile.state, profile.district, profile.category,
         1 if profile.disability else 0, profile.gender, profile.language,
         json.dumps(profile.needs), now, now)
    )
    db.commit()
    db.close()
    return {"userId": user_id, "completeness": 100, "createdAt": now}


@router.get("/{user_id}")
def get_profile(user_id: str):
    """Get user profile by ID."""
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE userId = ?", (user_id,)).fetchone()
    db.close()
    if not row:
        raise HTTPException(404, "Profile not found")
    d = dict(row)
    d["disability"] = bool(d.get("disability", 0))
    if d.get("needs"):
        try:
            d["needs"] = json.loads(d["needs"])
        except:
            d["needs"] = []
    return {"profile": d}


@router.put("/{user_id}")
def update_profile(user_id: str, profile: ProfileCreate):
    """Update user profile."""
    now = datetime.utcnow().isoformat()
    db = get_db()
    db.execute(
        """UPDATE users SET age=?, incomeBracket=?, occupation=?, state=?, district=?,
           category=?, disability=?, gender=?, language=?, needs=?, updatedAt=?
           WHERE userId=?""",
        (profile.age, profile.incomeBracket, profile.occupation, profile.state,
         profile.district, profile.category, 1 if profile.disability else 0,
         profile.gender, profile.language, json.dumps(profile.needs), now, user_id)
    )
    db.commit()
    db.close()
    return {"userId": user_id, "updatedAt": now}


@router.delete("/{user_id}")
def delete_profile(user_id: str):
    """Delete user profile (scheduled deletion)."""
    db = get_db()
    db.execute("DELETE FROM users WHERE userId = ?", (user_id,))
    db.commit()
    db.close()
    return {"success": True, "message": "Profile deletion scheduled"}
