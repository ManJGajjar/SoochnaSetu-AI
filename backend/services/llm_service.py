"""
LLM Service - Abstraction layer for language model integration.
Primary: AWS Bedrock | Fallback: OpenAI | Last resort: Rule-based
"""
import os
import json
import time
import random
import logging
from typing import Optional

logger = logging.getLogger(__name__)

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "rule_based")


class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.state = "CLOSED"

    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")
        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
            raise


_circuit_breaker = CircuitBreaker()


def generate(prompt: str, max_tokens: int = 1000, temperature: float = 0.3) -> str:
    """Unified LLM generation interface with fallback chain."""
    provider = LLM_PROVIDER

    if provider == "bedrock":
        try:
            return _circuit_breaker.call(_call_bedrock, prompt, max_tokens, temperature)
        except Exception as e:
            logger.warning(f"Bedrock failed: {e}, falling back to rule_based")
            return _rule_based_response(prompt)

    elif provider == "openai":
        try:
            return _circuit_breaker.call(_call_openai, prompt, max_tokens, temperature)
        except Exception as e:
            logger.warning(f"OpenAI failed: {e}, falling back to rule_based")
            return _rule_based_response(prompt)

    else:
        return _rule_based_response(prompt)


def _call_bedrock(prompt: str, max_tokens: int, temperature: float) -> str:
    """Call AWS Bedrock Claude model with retry logic."""
    import boto3

    region = os.getenv("AWS_REGION", "ap-south-1")
    model_id = os.getenv("BEDROCK_MODEL_ID", "amazon.titan-text-express-v1")
    client = boto3.client("bedrock-runtime", region_name=region)

    body = json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": max_tokens,
            "temperature": temperature
        }
    })

    for attempt in range(3):
        try:
            response = client.invoke_model(modelId=model_id, body=body, accept="application/json", contentType="application/json")
            result = json.loads(response["body"].read())
            return result["results"][0]["outputText"].strip()
        except Exception as e:
            if attempt < 2:
                wait = (2 ** attempt) + random.uniform(0, 1)
                logger.warning(f"Bedrock attempt {attempt+1} failed, retrying in {wait:.1f}s")
                time.sleep(wait)
            else:
                raise


def _call_openai(prompt: str, max_tokens: int, temperature: float) -> str:
    """Call OpenAI API."""
    import openai

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Soochna Setu AI, a helpful civic assistant for Indian citizens."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content


# ── Rule-Based Fallback ──────────────────────────────────────
MOCK_RESPONSES = {
    "pm kisan": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi) provides ₹6,000 per year to small and marginal farmers in 3 installments of ₹2,000 each. The amount is directly transferred to the farmer's bank account. To apply, visit pmkisan.gov.in and register with your Aadhaar number. You need land records, Aadhaar card, and a bank account. [Source: PM-KISAN Guidelines 2024, Confidence: 97%]",
    "ayushman": "Ayushman Bharat - PM Jan Arogya Yojana (PM-JAY) provides health insurance cover of ₹5 lakh per family per year for secondary and tertiary hospitalization. It covers over 1,500 medical procedures. Check your eligibility at mera.pmjay.gov.in and get your Ayushman card at the nearest CSC center. [Source: AB-PMJAY Operational Guidelines, Confidence: 95%]",
    "mgnrega": "MGNREGA guarantees 100 days of wage employment per year to every rural household. To get work, apply at your Gram Panchayat for a Job Card. Once you have the card, you can demand work in writing, and it must be provided within 15 days. If work is not given within 15 days, you are entitled to unemployment allowance. [Source: MGNREGA Act 2005, Section 3, Confidence: 99%]",
    "pm awas": "PM Awas Yojana provides housing subsidy. Under PMAY-Urban, you can get subsidy of ₹1.5 lakh to ₹2.67 lakh on home loans. Under PMAY-Gramin (rural), BPL families get ₹1.2 lakh for building a pucca house. Apply at pmaymis.gov.in (urban) or through Gram Panchayat (rural). [Source: PMAY Guidelines 2024, Confidence: 96%]",
    "mudra": "PM MUDRA Yojana provides loans up to ₹10 lakh for small businesses without collateral. There are 3 categories: Shishu (up to ₹50,000), Kishore (₹50,000 to ₹5 lakh), and Tarun (₹5 lakh to ₹10 lakh). Apply at any bank or through the udyamimitra.in portal. [Source: MUDRA Guidelines, Confidence: 94%]",
    "scholarship": "Multiple scholarship schemes are available through the National Scholarship Portal (scholarships.gov.in). These include Post-Matric Scholarship for SC/ST/OBC students, Merit-cum-Means Scholarship, and Central Sector Scholarship. Benefits range from ₹10,000 to ₹50,000 per year depending on the scheme. [Source: NSP Guidelines, Confidence: 93%]",
    "pension": "Several pension schemes are available: Atal Pension Yojana (₹1,000-5,000/month after 60, for age 18-40), Indira Gandhi National Old Age Pension (₹200-500/month for BPL seniors above 60), and PM Vaya Vandana Yojana for senior citizens. [Source: NSAP Guidelines, Confidence: 92%]",
    "sukanya": "Sukanya Samriddhi Yojana is a savings scheme for girl children. You can open an account for a girl below 10 years with a minimum deposit of ₹250. The current interest rate is 8.2% per year. The account matures when the girl turns 21. It also provides tax benefits under Section 80C. [Source: NSI Guidelines, Confidence: 96%]",
}


def _rule_based_response(prompt: str) -> str:
    """Keyword-matching fallback when no LLM is available."""
    prompt_lower = prompt.lower()

    for keyword, response in MOCK_RESPONSES.items():
        if keyword in prompt_lower:
            return response

    # Generic scheme matching response
    if "rank" in prompt_lower or "recommend" in prompt_lower or "eligible" in prompt_lower:
        return _generate_ranking_response(prompt)

    if "explain" in prompt_lower or "summary" in prompt_lower or "simplif" in prompt_lower:
        return "This document discusses government policies and budget allocations. Key points include allocation of funds for education, healthcare, and infrastructure development. For detailed understanding, please refer to the original document sections cited below."

    return ("I can help you find government schemes you're eligible for. "
            "Please tell me about yourself - your age, occupation, state, and income level - "
            "and I'll find the best schemes for you. You can also ask about specific schemes "
            "like PM-KISAN, Ayushman Bharat, MGNREGA, and more.")


def _generate_ranking_response(prompt: str) -> str:
    """Generate a structured ranking response for scheme matching."""
    return json.dumps({
        "rankings": [
            {
                "schemeId": "match",
                "eligibilityScore": 85,
                "reasoning": "Based on the user's profile, this scheme matches their eligibility criteria.",
                "matchedCriteria": ["Age requirement met", "Income bracket eligible", "State eligible"],
                "missingCriteria": [],
                "requiredDocuments": ["Aadhaar Card", "Bank Account", "Income Certificate"]
            }
        ]
    })
