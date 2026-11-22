
import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from jyotish import RASHIS_EN

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL = "gemini-3.7-flash"

PROMPT = """You are writing the daily rashifal for a Nepali astrology app.

Date: {date}

Write one short reading for each of the 12 moon signs (chandra rashi).
Each reading is 2 or 3 sentences covering mood, work and relationships.
Keep it warm, general and encouraging.

Rules:
- Never predict death, illness, pregnancy or any medical outcome.
- Never promise money, exam results or job offers.
- Write the Nepali and the English independently, each natural in its own
  language. Do not translate one into the other.

Return JSON in exactly this shape:
{{"readings": [{{"rashi": "Mesh", "ne": "...", "en": "..."}}]}}

Use these rashi names, in this order: {names}
"""


def generate_daily(date_str):
    prompt = PROMPT.format(date=date_str, names=", ".join(RASHIS_EN))

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )

    return json.loads(response.text)
