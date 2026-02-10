import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Reddit API
    REDDIT_CLIENT_ID: str
    REDDIT_CLIENT_SECRET: str
    REDDIT_USER_AGENT: str = "LeadScanner/2.0"

    # AI API
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Notification
    DISCORD_WEBHOOK_URL: str

    # Database (Defaults to SQLite file in the current directory)
    DATABASE_URL: str = "sqlite:///./leads.db"

    # Application Config
    # We use a set for O(1) lookups
    TARGET_SUBREDDITS: str = "marketing+entrepreneur+saas+smallbusiness+startups"
    KEYWORDS: List[str] = [
        "looking for", "recommend", "best tool", "struggling with",
        "how do i", "alternative to", "vs", "leads", "automation"
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()