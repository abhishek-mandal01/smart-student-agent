import os
from pathlib import Path

from dotenv import load_dotenv


# Load the project .env if present
ROOT = Path(__file__).resolve().parents[1]
DOTENV_PATH = ROOT / ".env"
if DOTENV_PATH.exists():
    load_dotenv(dotenv_path=DOTENV_PATH)
else:
    load_dotenv()


# Simple environment-backed settings (no pydantic dependency required)
OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
DEFAULT_USER_ID: str = os.getenv("DEFAULT_USER_ID", "user_1")
VECTOR_DIR: str = os.getenv("VECTOR_DIR", "./vector_db")


def require_openai_key() -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Add it to .env or set the environment variable."
        )
    return OPENAI_API_KEY


# Backwards-compatible settings object for code expecting `settings.X`
class _Settings:
    OPENAI_API_KEY = OPENAI_API_KEY
    DEFAULT_USER_ID = DEFAULT_USER_ID
    VECTOR_DIR = VECTOR_DIR


settings = _Settings()
