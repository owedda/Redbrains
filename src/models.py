# src/models.py
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Lead(Base):
    __tablename__ = 'leads'

    id = Column(String, primary_key=True)  # Reddit Post ID
    title = Column(String)
    url = Column(String)
    lead_score = Column(Integer)
    ai_analysis = Column(Text)
    draft_reply = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_notified = Column(Boolean, default=False)