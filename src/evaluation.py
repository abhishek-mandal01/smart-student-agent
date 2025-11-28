import logging
logger = logging.getLogger(__name__)

def evaluate_improvement(baseline_score: float, recent_score: float):
    improvement = recent_score - baseline_score
    logger.info("Evaluate improvement baseline=%.2f recent=%.2f imp=%.2f", baseline_score, recent_score, improvement)
    return {"baseline": baseline_score, "recent": recent_score, "improvement": improvement}
