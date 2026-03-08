from pydantic import BaseModel
from typing import Optional, List


class EligibilityCriteria(BaseModel):
    ageMin: Optional[int] = None
    ageMax: Optional[int] = None
    incomeBrackets: List[str] = []
    occupations: List[str] = []
    states: List[str] = ["ALL"]
    categories: List[str] = []
    requiresDisability: Optional[bool] = None
    gender: Optional[str] = None
    additionalCriteria: Optional[str] = None


class Scheme(BaseModel):
    schemeId: str
    name: str
    nameLocal: Optional[str] = None
    description: str
    simpleDescription: Optional[str] = None
    analogy: Optional[str] = None
    category: str
    state: str = "ALL"
    eligibility: EligibilityCriteria
    benefits: List[str] = []
    benefitAmount: Optional[str] = None
    benefitType: Optional[str] = None
    requiredDocuments: List[str] = []
    applicationProcess: List[str] = []
    officialLink: str = ""
    helplineNumber: Optional[str] = None
    deadline: Optional[str] = None
    commonRejectionReasons: List[str] = []
    tags: List[str] = []
    lastUpdated: str = ""
    isActive: bool = True


class RankedScheme(BaseModel):
    scheme: Scheme
    eligibilityScore: int  # 0-100
    reasoning: str
    matchedCriteria: List[str] = []
    missingCriteria: List[str] = []
    requiredDocuments: List[str] = []
    estimatedApprovalTime: Optional[str] = None


class SchemeSearchQuery(BaseModel):
    query: str
    category: Optional[str] = None
    state: Optional[str] = None
    limit: int = 10
