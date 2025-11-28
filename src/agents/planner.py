from typing import Dict, Any
from ..llm import llm
import logging

logger = logging.getLogger(__name__)

def create_study_plan(user_id: str, deadlines: list, preferences: Dict[str, Any] = None) -> Dict:
    """
    Planner agent: produce a structured plan from deadlines and user prefs.
    Returns dict with structured 'plan' key (list of blocks).
    """
    pref_text = f"Preferences: {preferences}" if preferences else ""
    prompt = f"""
You are a study scheduler assistant.
User ID: {user_id}
Deadlines: {deadlines}
{pref_text}

Produce a 7-day study plan. For each day list study blocks as:
- date (YYYY-MM-DD), subject, duration_minutes, objective.
Return JSON only, with key "plan" a list of blocks.
"""
    raw = llm.call(prompt)
    # naive handling: try to parse JSON if LLM returned JSON; else return a mock
    import json
    try:
        parsed = json.loads(raw)
        return parsed
    except Exception:
        logger.warning("Planner returned non-json; returning a sample plan")
        plan = [
            {"date":"2025-11-29","subject":"Mathematics","duration_minutes":60,"objective":"Practice calculus problems"},
            {"date":"2025-11-30","subject":"Biology","duration_minutes":45,"objective":"Summarize chapter 3"},
        ]
        return {"plan": plan, "raw": raw}
