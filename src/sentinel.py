# src/sentinel.py
import json
import redis
import logging
from src.config import settings
from src.services.reddit_client import get_reddit_client

# Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Sentinel")

# Connect to Redis
redis_client = redis.Redis(host='redis', port=6379, db=0)


def start_listening():
    reddit = get_reddit_client()
    subreddit = reddit.subreddit(settings.TARGET_SUBREDDITS)

    logger.info(f"🎧 Sentinel started. Monitoring: {settings.TARGET_SUBREDDITS}")

    for post in subreddit.stream.submissions(skip_existing=True):
        try:
            # 1. Quick Keyword Filter (Fast Sieve)
            # We do this here to avoid filling the Queue with junk
            full_text = (post.title + " " + post.selftext).lower()
            if any(k in full_text for k in settings.KEYWORDS):
                # 2. Serialize and Push to Queue
                payload = {
                    "id": post.id,
                    "title": post.title,
                    "text": post.selftext,
                    "url": post.url,
                    "author": str(post.author)
                }

                # Push to 'post_queue' list in Redis
                redis_client.lpush('post_queue', json.dumps(payload))
                logger.info(f"Detected potential lead: {post.id} -> Pushed to Queue")

        except Exception as e:
            logger.error(f"Error in stream: {e}")


if __name__ == "__main__":
    start_listening()