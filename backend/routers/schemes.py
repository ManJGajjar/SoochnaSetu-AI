"""Schemes Router - Full implementation with real matching."""
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from db.database import get_all_schemes, get_scheme_by_id
from services.scheme_matcher import get_recommendations
from models.user import UserProfile

router = APIRouter()


class MatchRequest(BaseModel):
    age: int
    incomeBracket: str
    occupation: str
    state: str
    category: str = "General"
    district: Optional[str] = None
    disability: bool = False
    disabilityType: Optional[str] = None
    gender: Optional[str] = None
    language: str = "en"
    needs: List[str] = []


@router.get("/")
def list_schemes(
    category: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
):
    """List all active schemes with optional filters."""
    schemes = get_all_schemes()

    if category:
        schemes = [s for s in schemes if s.get("category", "").lower() == category.lower()]
    if state:
        def _state_match(s):
            elig = s.get("eligibility", {})
            if isinstance(elig, str):
                import json as _j
                try: elig = _j.loads(elig)
                except: elig = {}
            st = elig.get("states", ["ALL"])
            return "ALL" in st or state in st
        schemes = [s for s in schemes if _state_match(s)]
    if search:
        q = search.lower()
        schemes = [s for s in schemes if q in s.get("name", "").lower() or q in s.get("description", "").lower() or q in str(s.get("tags", [])).lower()]

    return {"count": len(schemes[:limit]), "schemes": schemes[:limit]}


@router.get("/{scheme_id}")
def get_scheme(scheme_id: str):
    """Get scheme detail by ID."""
    scheme = get_scheme_by_id(scheme_id)
    if not scheme:
        raise HTTPException(status_code=404, detail=f"Scheme {scheme_id} not found")
    return {"scheme": scheme}


@router.post("/match")
def match_schemes(profile: MatchRequest):
    """Match schemes to user profile using hybrid rule-based + scoring engine."""
    all_schemes = get_all_schemes()
    user = profile.model_dump()
    recommendations = get_recommendations(user, all_schemes)

    return {
        "count": len(recommendations),
        "profile": {
            "age": profile.age,
            "occupation": profile.occupation,
            "state": profile.state,
            "category": profile.category,
            "incomeBracket": profile.incomeBracket,
        },
        "recommendations": recommendations,
    }


@router.get("/{scheme_id}/apply-guide")
def apply_guide(scheme_id: str):
    """Get step-by-step application guide for a scheme."""
    scheme = get_scheme_by_id(scheme_id)
    if not scheme:
        raise HTTPException(status_code=404, detail=f"Scheme {scheme_id} not found")

    process = scheme.get("applicationProcess", [])
    docs = scheme.get("requiredDocuments", [])
    rejections = scheme.get("commonRejectionReasons", [])

    return {
        "schemeId": scheme_id,
        "schemeName": scheme.get("name"),
        "steps": process,
        "requiredDocuments": docs,
        "commonRejectionReasons": rejections,
        "officialLink": scheme.get("officialLink", ""),
        "helplineNumber": scheme.get("helplineNumber", ""),
    }
