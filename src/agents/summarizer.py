from typing import List
from ..llm import llm
import logging

logger = logging.getLogger(__name__)

def summarize_chunks(chunks: List[str]) -> str:
    """
    Summarizer agent: condense multiple text chunks into a short summary.
    """
    joined = "\n\n".join(chunks[:6])  # limit to first N chunks to keep prompt small

    prompt = f"""
You are an expert study assistant. Summarize the following text into clear,
easy-to-learn bullet points. Keep it concise and only retain important ideas.

Text:
{joined}
"""

    # Optional system-like prefix to improve consistency
    prompt = "You are a helpful student assistant.\n" + prompt

    summary = llm.call(prompt)
    logger.info("Generated summary len=%d", len(summary))
    return summary
