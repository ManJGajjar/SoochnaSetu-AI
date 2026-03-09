"""
Scheme Matcher - Hybrid rule-based + LLM matching per design doc.
Step 1: Rule-based filter (eliminates 80-90% non-eligible schemes)
Step 2: LLM reranker (adds reasoning and personalized scoring)
"""
import json
import logging
from typing import List, Dict, Any, Optional
from services.llm_service import generate

logger = logging.getLogger(__name__)


def rule_based_filter(user_profile: Dict, all_schemes: List[Dict]) -> List[Dict]:
    """Filter schemes by hard eligibility constraints. Zero hallucination."""
    matched = []

    user_age = user_profile.get("age", 0)
    user_income = user_profile.get("incomeBracket", "")
    user_occupation = user_profile.get("occupation", "").lower()
    user_state = user_profile.get("state", "")
    user_category = user_profile.get("category", "General")
    user_gender = user_profile.get("gender", "")
    user_disability = user_profile.get("disability", False)

    for scheme in all_schemes:
        if not scheme.get("isActive", True):
            continue

        elig = scheme.get("eligibility", {})
        if isinstance(elig, str):
            try:
                elig = json.loads(elig)
            except json.JSONDecodeError:
                elig = {}

        # Age filter
        age_min = elig.get("ageMin")
        age_max = elig.get("ageMax")
        if age_min and user_age < age_min:
            continue
        if age_max and user_age > age_max:
            continue

        # Income filter
        income_brackets = elig.get("incomeBrackets", [])
        if income_brackets and user_income and user_income not in income_brackets:
            continue

        # Occupation filter
        occupations = elig.get("occupations", [])
        if occupations:
            occ_match = False
            for occ in occupations:
                if occ.lower() in user_occupation or user_occupation in occ.lower():
                    occ_match = True
                    break
            if not occ_match:
                continue

        # State filter
        states = elig.get("states", ["ALL"])
        if states and "ALL" not in states and user_state not in states:
            continue

        # Category filter
        categories = elig.get("categories", [])
        if categories and user_category not in categories:
            continue

        # Gender filter
        scheme_gender = elig.get("gender")
        if scheme_gender and user_gender and scheme_gender.lower() != user_gender.lower():
            continue

        # Disability filter
        requires_disability = elig.get("requiresDisability", False)
        if requires_disability and not user_disability:
            continue

        matched.append(scheme)

    return matched


def calculate_eligibility_score(user_profile: Dict, scheme: Dict) -> int:
    """Calculate eligibility score 0-100 per design doc formula."""
    base_score = 70  # Base score for passing all hard filters

    elig = scheme.get("eligibility", {})
    if isinstance(elig, str):
        try:
            elig = json.loads(elig)
        except json.JSONDecodeError:
            elig = {}

    # Boost for exact occupation match
    occupations = elig.get("occupations", [])
    user_occ = user_profile.get("occupation", "").lower()
    if occupations:
        for occ in occupations:
            if occ.lower() == user_occ:
                base_score += 10
                break

    # Boost for category preference
    categories = elig.get("categories", [])
    if categories and user_profile.get("category") in categories:
        base_score += 5

    # Boost for income match (lower income = higher priority for welfare)
    income = user_profile.get("incomeBracket", "")
    if income in ("BPL", "0-2.5L"):
        base_score += 10
    elif income == "2.5-5L":
        base_score += 5

    # Boost for state-specific schemes
    states = elig.get("states", ["ALL"])
    if states and "ALL" not in states and user_profile.get("state") in states:
        base_score += 5

    return max(0, min(100, base_score))


def get_matched_criteria(user_profile: Dict, scheme: Dict) -> List[str]:
    """List criteria the user satisfies."""
    matched = []
    elig = scheme.get("eligibility", {})
    if isinstance(elig, str):
        try:
            elig = json.loads(elig)
        except json.JSONDecodeError:
            elig = {}

    age_min = elig.get("ageMin")
    age_max = elig.get("ageMax")
    user_age = user_profile.get("age", 0)
    if age_min or age_max:
        matched.append(f"Age: You are {user_age}, scheme requires {age_min or 'any'}-{age_max or 'any'}")

    occupations = elig.get("occupations", [])
    if occupations:
        matched.append(f"Occupation: Your occupation matches ({user_profile.get('occupation')})")
    else:
        matched.append("Occupation: Open to all occupations")

    income_brackets = elig.get("incomeBrackets", [])
    if income_brackets:
        matched.append(f"Income: Your income bracket ({user_profile.get('incomeBracket')}) is eligible")

    matched.append(f"State: {'All India scheme' if 'ALL' in elig.get('states', ['ALL']) else 'State eligible'}")

    return matched


def get_missing_criteria(user_profile: Dict, scheme: Dict) -> List[str]:
    """List criteria the user doesn't fully meet (soft criteria)."""
    missing = []
    elig = scheme.get("eligibility", {})
    if isinstance(elig, str):
        try:
            elig = json.loads(elig)
        except json.JSONDecodeError:
            elig = {}

    categories = elig.get("categories", [])
    if categories and user_profile.get("category") not in categories:
        missing.append(f"Category preference: Scheme prefers {', '.join(categories)}")

    return missing


def generate_reasoning(user_profile: Dict, scheme: Dict, score: int) -> str:
    """Generate personalized reasoning for why a scheme matches."""
    occupation = user_profile.get("occupation", "citizen")
    state = user_profile.get("state", "India")
    age = user_profile.get("age", 0)
    income = user_profile.get("incomeBracket", "")
    name = scheme.get("name", "")
    benefit = scheme.get("benefitAmount", "")

    import os
    if os.getenv("LLM_PROVIDER") == "bedrock":
        try:
            prompt = (f"You are a helpful government scheme advisor. "
                      f"Explain in 2 short sentences why a user (Age: {age}, Occupation: {occupation}, "
                      f"State: {state}, Income: {income}) qualifies for the '{name}' scheme. "
                      f"The scheme provides: {benefit}. "
                      f"Keep the tone encouraging, personalize it to their profile, and do not use bullet points.")
            reasoning = generate(prompt, max_tokens=150)
            if reasoning and len(reasoning) > 10:
                return reasoning.strip()
        except Exception as e:
            logger.error(f"LLM reasoning failed: {e}")

    return (f"As a {occupation} in {state}, aged {age}, with income in the {income} bracket, "
            f"you match {score}% of {name}'s eligibility criteria. "
            f"This scheme offers {benefit}. "
            f"Based on your profile, you have a strong chance of approval.")


def get_recommendations(user_profile: Dict, all_schemes: List[Dict]) -> List[Dict]:
    """Full recommendation pipeline: rule filter → score → rank → enrich."""
    # Step 1: Rule-based filter
    filtered = rule_based_filter(user_profile, all_schemes)

    if not filtered:
        return []

    # Step 2: Score and rank
    ranked = []
    for scheme in filtered:
        score = calculate_eligibility_score(user_profile, scheme)
        matched = get_matched_criteria(user_profile, scheme)
        missing = get_missing_criteria(user_profile, scheme)

        docs = scheme.get("requiredDocuments", [])
        if isinstance(docs, str):
            try:
                docs = json.loads(docs)
            except json.JSONDecodeError:
                docs = []

        ranked.append({
            "scheme": scheme,
            "eligibilityScore": score,
            "reasoning": "",  # Will be enriched concurrently
            "matchedCriteria": matched,
            "missingCriteria": missing,
            "requiredDocuments": docs,
        })

    # Sort by eligibility score descending
    ranked.sort(key=lambda x: x["eligibilityScore"], reverse=True)
    top_ranked = ranked[:10]

    # Generate reasoning concurrently for the top results to save time
    import concurrent.futures
    def enrich_reasoning(item):
        item["reasoning"] = generate_reasoning(user_profile, item["scheme"], item["eligibilityScore"])
        return item
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        top_ranked = list(executor.map(enrich_reasoning, top_ranked))

    # Return top 10
    return top_ranked
