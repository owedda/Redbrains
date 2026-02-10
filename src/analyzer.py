# src/analyzer.py
import json
import redis
import time
import logging
from src.services.ai_engine import analyze_lead
from src.services.notifier import send_discord_alert
from src.database import SessionLocal, init_db
from src.models import Lead

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Analyzer")

redis_client = redis.Redis(host='redis', port=6379, db=0)


def process_job(payload):
    data = json.loads(payload)

    # 1. Check DB: Have we processed this already?
    session = SessionLocal()
    if session.query(Lead).filter_by(id=data['id']).first():
        logger.info(f"Skipping duplicate: {data['id']}")
        session.close()
        return

    # 2. AI Analysis
    logger.info(f"Analyzing post: {data['title'][:30]}...")
    analysis_result = analyze_lead(data['title'], data['text'])

    if analysis_result['score'] >= 75:
        # 3. Save to DB
        new_lead = Lead(
            id=data['id'],
            title=data['title'],
            url=data['url'],
            lead_score=analysis_result['score'],
            ai_analysis=analysis_result['reason'],
            draft_reply=analysis_result['draft_reply']
        )
        session.add(new_lead)
        session.commit()

        # 4. Notify
        send_discord_alert(new_lead)
        logger.info(f"🔥 HOT LEAD FOUND: {data['id']}")
    else:
        logger.info(f"Lead score too low ({analysis_result['score']}). Discarding.")

    session.close()


def start_worker():
    logger.info("🧠 Analyzer Worker started. Waiting for jobs...")
    init_db()  # Create tables if not exist

    while True:
        # Blocking pop: waits until an item is available in the list
        # Returns tuple (queue_name, data)
        _, payload = redis_client.brpop('post_queue')

        try:
            process_job(payload)
        except Exception as e:
            logger.error(f"Job failed: {e}")


if __name__ == "__main__":
    start_worker()