# Smart Student Agent

Lightweight demo assistant for studying: ingests lecture PDFs, summarizes content, and generates short quizzes.

**Quick summary:**
- Python + Streamlit demo app
- Uses OpenAI for LLM + embeddings
- FAISS vector store for local similarity search
- Simple in-memory `MemoryBank` for user session state (see `src/memory.py`)

**Requirements**
- Python 3.11+
- Recommended: create a virtual environment (included in repo setup instructions)

**Setup (Windows PowerShell)**
1. Create and activate a venv (project root):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Add your secrets into a `.env` file at the project root (example provided):

```text
OPENAI_API_KEY=sk-...your-key...
DEFAULT_USER_ID=user_1
```

Notes:
- The repository already contains a `.env` template and `.gitignore` ignores `.env` and `.venv`.
- For production or CI, store `OPENAI_API_KEY` in your CI/host secrets rather than `.env`.

**Run (local demo)**
- Launch the Streamlit app after activating the venv:

```powershell
streamlit run app.py
```

Or on Unix/macOS (if you prefer):

```bash
./run_local.sh
```

**Files & structure**
- `app.py` — Streamlit UI that wires together the agents.
- `src/config.py` — Loads environment variables (via `python-dotenv`) and exposes `settings`.
- `src/llm.py` — Small wrapper for OpenAI usage (chat & embeddings).
- `src/memory.py` — `MemoryBank` in-memory store (per-user dict with `_last_update`).
- `src/agents/` — agent modules (`planner.py`, `summarizer.py`, `quiz_agent.py`).
- `src/tools/` — helpers for PDF ingest and vector store (`pdf_ingest.py`, `vectorstore.py`).
- `vector_db/` — local FAISS index files (created by the app).

**Memory details**
- `src/memory.py` implements a tiny in-memory `MemoryBank` used for demo runs. It stores a dictionary per `user_id` and adds a `_last_update` timestamp on writes. Replace this with a persistent DB for production workloads.

**Editor configuration**
- A VS Code settings file was added at `.vscode/settings.json` to point the editor to the project's venv and include `src/` in analysis paths. If you use VS Code, pick the interpreter at the bottom-right if needed.

**Troubleshooting**
- If your editor reports "import X could not be resolved", ensure the workspace Python interpreter is set to `./.venv/Scripts/python.exe` or restart the editor to pick up `.vscode/settings.json`.
- If the app can't find `OPENAI_API_KEY`, ensure the `.env` file is present or the variable is set in your environment. `src/config.py` provides `require_openai_key()` to fail fast at startup.

**License & contact**
- All Rights reserved
