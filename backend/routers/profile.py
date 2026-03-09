"""Profile Router - User profile CRUD."""
import uuid
import json
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from db.database import get_table

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
    table = get_table('SoochnaSetu-Users')
    
    item = profile.model_dump()
    item['userId'] = user_id
    item['createdAt'] = now
    item['updatedAt'] = now
    
    table.put_item(Item=item)
    return {"userId": user_id, "completeness": 100, "createdAt": now}

@router.get("/{user_id}")
def get_profile(user_id: str):
    """Get user profile by ID."""
    table = get_table('SoochnaSetu-Users')
    response = table.get_item(Key={'userId': user_id})
    item = response.get('Item')
    
    if not item:
        raise HTTPException(404, "Profile not found")
        
    def convert_decimals(obj):
        from decimal import Decimal
        if isinstance(obj, list):
            return [convert_decimals(i) for i in obj]
        elif isinstance(obj, dict):
            return {k: convert_decimals(v) for k, v in obj.items()}
        elif isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return obj
        
    d = convert_decimals(item)
    d["disability"] = bool(d.get("disability", False))
    return {"profile": d}

@router.put("/{user_id}")
def update_profile(user_id: str, profile: ProfileCreate):
    """Update user profile."""
    now = datetime.utcnow().isoformat()
    table = get_table('SoochnaSetu-Users')
    
    item = profile.model_dump()
    item["userId"] = user_id
    item["updatedAt"] = now
    
    existing = table.get_item(Key={'userId': user_id}).get('Item', {})
    if 'createdAt' in existing:
        item['createdAt'] = existing['createdAt']
    else:
        item['createdAt'] = now
        
    table.put_item(Item=item)
    return {"userId": user_id, "updatedAt": now}

@router.delete("/{user_id}")
def delete_profile(user_id: str):
    """Delete user profile."""
    table = get_table('SoochnaSetu-Users')
    table.delete_item(Key={'userId': user_id})
    return {"success": True, "message": "Profile deletion scheduled"}
