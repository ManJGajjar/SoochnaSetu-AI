"""Translator service - Multi-language support via LLM."""
import logging
from services.llm_service import generate

logger = logging.getLogger(__name__)

LANG_MAP = {
    "hi": "Hindi", "en": "English", "gu": "Gujarati", "ta": "Tamil",
    "te": "Telugu", "bn": "Bengali", "mr": "Marathi", "kn": "Kannada",
    "ml": "Malayalam", "pa": "Punjabi", "or": "Odia", "as": "Assamese",
}


def translate(text: str, target_lang: str) -> str:
    """Translate text to target language using LLM."""
    if target_lang == "en":
        return text
    lang_name = LANG_MAP.get(target_lang, "Hindi")
    prompt = f"Translate the following text to {lang_name}. Keep technical terms and scheme names as-is.\n\nText: {text}"
    try:
        return generate(prompt, max_tokens=1000)
    except Exception as e:
        logger.warning(f"Translation failed: {e}")
        return text
