from google import genai
from fastapi import HTTPException
import os

from config import settings
from models import Suspect, CaseTemplate

# Fail early with a clear message rather than a cryptic 500 on first use.
_PLACEHOLDER = "your_api_key_here"

_api_key = settings.gemini_api_key

if not _api_key or _api_key == _PLACEHOLDER:
    _client = None
else:
    _client = genai.Client(api_key=_api_key)


def ask_ai(prompt: str) -> str:
    if _client is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "Gemini API key not configured. "
                "Set GEMINI_API_KEY in your .env file or as an environment variable, "
                "then restart the server."
            ),
        )
    response = _client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text


TOPIC_QUESTIONS = {
    "alibi": "Where were you during the time of the murder?",
    "relationship": "What was your relationship with the victim?",
    "saw": "Did you see or hear anything unusual tonight?",
    "rumor": "Do you know anything about what the others were doing?",
}


def build_prompt(suspect: Suspect, case: CaseTemplate, topic: str) -> str:
    # Load template from file
    template_path = os.path.join(os.path.dirname(__file__), "prompts", "interrogation_v1.txt")
    with open(template_path, "r") as f:
        template = f.read()

    fact = case.suspect_facts[suspect.key][topic]
    question = TOPIC_QUESTIONS[topic]

    evasive_instruction = ""
    if fact["evasive"]:
        evasive_instruction = (
            f"On this particular topic you are uncomfortable, for personal reasons "
            f"tied to '{fact['reason']}'. You do not lie or invent facts, but you are "
            f"reluctant, indirect, or reframe the question rather than answering it "
            f"head-on. Let your personality shape exactly how that reluctance shows."
        )

    prompt = template.format(
        name=suspect.name,
        occupation=suspect.occupation,
        personality=suspect.personality,
        background=suspect.background,
        location=case.location,
        window=case.window,
        victim=case.victim,
        truth=fact["truth"],
        evasive_instruction=evasive_instruction,
        question=question,
    )
    return prompt


def interrogate(case: CaseTemplate, suspect: Suspect, topic: str):
    prompt = build_prompt(suspect, case, topic)
    return ask_ai(prompt)

