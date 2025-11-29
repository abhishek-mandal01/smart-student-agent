import os
from pathlib import Path
import logging

import google.generativeai as genai
from dotenv import load_dotenv

# Load .env from project root if present, then prefer environment variables.
ROOT = Path(__file__).resolve().parents[1]
DOTENV_PATH = ROOT / ".env"
if DOTENV_PATH.exists():
    load_dotenv(dotenv_path=DOTENV_PATH)
else:
    # call load_dotenv() to allow environment-based loading if present elsewhere
    load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    logging.warning(
        "GOOGLE_API_KEY not found in environment or .env. Configure `genai` with a key for full functionality."
    )

class LLM:
    def __init__(self):
        # Use a supported Gemini model; update here if your account has different model names
        # Use the fully-qualified model id discovered by `scripts/list_models.py`
        self.model = genai.GenerativeModel("models/gemini-2.5-pro")  # Chat + summarize
    
    def call(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text
    
    def embed_texts(self, texts):
        embeddings = []
        for t in texts:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=t
            )
            embeddings.append(result["embedding"])
        return embeddings


# Module-level LLM instance for easy imports from other modules
llm = LLM()
