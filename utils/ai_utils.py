# ai_utils.py
# Optional AI enrichment module for Wisdom Layer agents

import os
import openai
import hashlib
import json

# Optional: set this via environment variable
openai.api_key = os.getenv("")

CACHE_FILE = "data/ai_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def hash_prompt(prompt):
    return hashlib.sha256(prompt.encode()).hexdigest()

def get_intention_from_ai(text, cache_enabled=True):
    prompt = f"""
    Classify the following technical message by INTENTION:
    Message: "{text}"
    Choose one: Positive, Neutral, or Negative
    Answer:
    """
    key = hash_prompt(prompt)
    cache = load_cache() if cache_enabled else {}

    if key in cache:
        return cache[key]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert DevOps system analyst."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10,
            temperature=0.2,
        )
        reply = response.choices[0].message["content"].strip()
        intention = reply.split()[0].capitalize()

        if intention not in ["Positive", "Neutral", "Negative"]:
            intention = "Neutral"

        if cache_enabled:
            cache[key] = intention
            save_cache(cache)

        return intention

    except Exception as e:
        print(f"[AI ERROR] {e}")
        return "Neutral"  # fallback
