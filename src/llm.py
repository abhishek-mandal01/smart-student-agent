# src/llm.py
import logging
from typing import List
from openai import OpenAI
from .config import settings

logger = logging.getLogger(__name__)

# Create a client using openai>=1.0.0 interface
# It will use the supplied API key (or rely on env var)
_client = OpenAI(api_key=settings.OPENAI_API_KEY)

class LLM:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.client = _client

    def call(self, prompt: str, max_tokens: int = 512, temperature: float = 0.2) -> str:
        """
        Use the new OpenAI client chat completions API.
        """
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY not set in environment (.env).")

        logger.info("LLM.call model=%s prompt_len=%d", self.model, len(prompt))
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        # new API: response shape -> resp.choices[0].message.content
        text = ""
        try:
            text = resp.choices[0].message.content.strip()
        except Exception:
            # fallback to other shapes
            try:
                text = resp.choices[0].text.strip()
            except Exception:
                logger.exception("Unable to parse LLM response structure.")
                text = ""
        return text

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Use the new OpenAI embeddings API through the client.
        Returns list of embeddings (list of floats) in same order as texts.
        """
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY not set in environment (.env).")

        # The OpenAI client returns an object with .data where each entry has .embedding
        logger.info("Requesting embeddings for %d texts", len(texts))
        if not texts:
            return []

        resp = self.client.embeddings.create(
            model="text-embedding-3-small",  # more cost-effective; change if you want larger
            input=texts,
        )
        embs = [d.embedding for d in resp.data]
        return embs

# single shared instance for imports
llm = LLM()
