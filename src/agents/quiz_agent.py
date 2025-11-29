from typing import List, Dict
from ..llm import llm
import logging
import json

logger = logging.getLogger(__name__)

def generate_quiz(summary: str, n_questions: int = 5) -> List[Dict]:
    # Build a simple numbered format for questions (Q1:, Q2:, ...)
    format_lines = "\n".join([f"Q{i+1}:" for i in range(n_questions)])

    prompt = f"""
You are a helpful teacher. Create {n_questions} simple quiz questions based on the text below.
Format:
{format_lines}

Text:
{summary}
"""

    # Optional system-like prefix to improve consistency
    prompt = "You are a helpful student assistant.\n" + prompt

    raw = llm.call(prompt)
    try:
        data = json.loads(raw)
        return data
    except Exception:
        # fallback: return a simple dummy quiz
        logger.warning("Quiz agent returned non-json; returning fallback quiz")
        return [{"q":"What is X?","options":["A","B","C","D"],"answer":"A"}]
