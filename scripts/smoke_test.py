from pprint import pprint
import sys
sys.path.append('')

from src import orchestrator
from src.llm import llm

# Monkeypatch LLM to avoid external API calls
def fake_embed_texts(texts):
    # Return zero vectors with dim matching orchestrator vector store (1536)
    return [[0.0] * orchestrator.vector_store.dim for _ in texts]

def fake_call(prompt, max_tokens=512):
    # Return a short summary when asked to summarize; return JSON for quiz
    if 'Summarize' in prompt or 'expert study assistant' in prompt:
        return '• Key idea 1\n• Key idea 2'
    if 'Create' in prompt or 'You are a helpful teacher' in prompt:
        return '[{"q":"What is 1?","options":["A","B","C","D"],"answer":"A"}]'
    return 'OK'

llm.embed_texts = fake_embed_texts
llm.call = fake_call

pdfs = [
    'tmp/Experiential Learning IEE.pdf',
    'tmp/git-cheat-sheet-education.pdf',
]

out = orchestrator.run_session('test_user', pdfs)
pprint(out)
