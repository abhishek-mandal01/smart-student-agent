from typing import List, Dict
from ..llm import llm
import logging
import json

logger = logging.getLogger(__name__)

def generate_quiz(summary: str, n_questions: int = 5) -> List[Dict]:
    prompt = f"""From the following summary, create {n_questions} short multiple-choice questions (4 options each).
Return JSON array like: [{{"q":"...","options":["a","b","c","d"],"answer":"a"}}].
Summary:
{summary}
"""
    raw = llm.call(prompt, max_tokens=512)
    try:
        data = json.loads(raw)
        return data
    except Exception:
        # fallback: return a simple dummy quiz
        logger.warning("Quiz agent returned non-json; returning fallback quiz")
        return [{"q":"What is X?","options":["A","B","C","D"],"answer":"A"}]
