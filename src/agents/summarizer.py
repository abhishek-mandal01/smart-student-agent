from typing import List
from ..llm import llm
import logging

logger = logging.getLogger(__name__)

def summarize_chunks(chunks: List[str]) -> str:
    """
    Summarizer agent: condense multiple text chunks into a short summary.
    """
    joined = "\n\n".join(chunks[:6])  # limit to first N chunks to keep prompt small
    prompt = f"Summarize the following study material into concise notes (bulleted):\n\n{joined}\n\nProvide a concise, clear summary."
    summary = llm.call(prompt, max_tokens=800)
    logger.info("Generated summary len=%d", len(summary))
    return summary
