from .tools.pdf_ingest import extract_text_chunks
from .agents.summarizer import summarize_chunks
from .agents.quiz_agent import generate_quiz
from .memory import memory
from .tools.vectorstore import FaissVectorStore
from .llm import llm
from .config import settings
import logging

logger = logging.getLogger(__name__)
vector_store = FaissVectorStore(dim=1536, path=settings.VECTOR_DIR)

def run_session(user_id: str, pdf_paths: list):
    # 1) ingest
    all_chunks = []
    for p in pdf_paths:
        chunks = extract_text_chunks(p)
        all_chunks.extend(chunks)

    # 2) create embeddings and upsert into vectorstore
    # We'll batch the embeddings
    if all_chunks:
        embs = llm.embed_texts(all_chunks)
        metas = [{"source": p, "chunk_idx": i} for i, p in enumerate(all_chunks)]
        vector_store.upsert(embs, metas)

    # 3) summarize
    summary = summarize_chunks(all_chunks)
    # 4) quiz
    quiz = generate_quiz(summary, n_questions=5)

    # 5) update memory
    memory.write(user_id, {"last_summary": summary, "last_quiz": quiz})
    logger.info("Session completed for user=%s", user_id)
    return {"summary": summary, "quiz": quiz}
