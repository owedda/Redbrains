import praw
from src.config import settings

def get_reddit_client():
    """Returns an authenticated PRAW Reddit instance."""
    return praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_CLIENT_SECRET,
        user_agent=settings.REDDIT_USER_AGENT
    )