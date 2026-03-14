import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# RapidAPI — Google Translate (v1)
RAPIDAPI_URL = "https://google-translate113.p.rapidapi.com/api/v1/translator/text"

HEADERS = {
    "content-type": "application/x-www-form-urlencoded",
    "Accept-Encoding": "application/gzip",
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "google-translate113.p.rapidapi.com"
}


def translate_text(text, source="es", target="en"):
    """Translate a single string via RapidAPI Google Translate v1."""
    if not text or not text.strip():
        return ""

    payload = {
        "text": text,
        "from": source,
        "to": target
    }

    headers_clean = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "google-translate113.p.rapidapi.com"
    }

    try:
        for attempt in range(3):
            response = requests.post(RAPIDAPI_URL, data=payload, headers=headers_clean, timeout=15)
            if response.status_code == 429:
                # Rate limit hit, wait longer
                time.sleep(5)
                continue
                
            response.raise_for_status()
            result = response.json()
            
            if "trans" in result:
                return result["trans"]
            return str(result)
            
        return text # Return original if all attempts hit 429
    except Exception as e:
        print(f"-> Translation Error: {e}")
        return text  # fall back to original on failure


def translate_articles(articles):
    """Translate a list of (title, content) tuples from Spanish to English."""

    translated_data = []

    print()  # gap before English titles section
    print("-> Translated Headers:")
    for i, (title, content) in enumerate(articles):

        eng_title = translate_text(title)

        print(f"-> ENGLISH TITLE: {eng_title}")

        translated_data.append((title, eng_title, content, f"cover_{i+1}.jpg"))

        time.sleep(1)  # avoid RapidAPI rate limit (429)

    return translated_data