"""List available Gemini models for the configured account.

This script loads `./.env` (if present) and calls the GenAI client to list models.
Run with the project's venv Python:

    .\.venv\Scripts\python.exe scripts\list_models.py

"""
from pathlib import Path
import os
import json
from dotenv import load_dotenv

import google.generativeai as genai


ROOT = Path(__file__).resolve().parents[1]
dot = ROOT / ".env"
if dot.exists():
    load_dotenv(dotenv_path=dot)

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    print("GOOGLE_API_KEY not set in .env or environment. Set it and re-run to list models.")
    raise SystemExit(1)

genai.configure(api_key=API_KEY)

try:
    models_iter = genai.list_models()
    print("Available models:")
    count = 0
    for m in models_iter:
        count += 1
        # try to extract common attributes
        name = getattr(m, "name", None) or getattr(m, "model", None) or str(m)
        methods = getattr(m, "supported_methods", None) or getattr(m, "methods", None)
        print(f"- Model #{count}: {name}")
        if methods:
            try:
                print(f"  supported_methods: {list(methods)}")
            except Exception:
                print(f"  supported_methods: {methods}")
        else:
            # print a short repr if no methods attribute
            try:
                print(f"  repr: {repr(m)[:200]}")
            except Exception:
                print("  (no additional metadata)")
    if count == 0:
        print("No models returned by the API.")
except Exception as e:
    print("Failed to list models:", e)
    raise
