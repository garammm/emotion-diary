from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Integer, default=1)

    # Relationships
    entries = relationship("Entry", back_populates="user", cascade="all, delete-orphan")

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="entries")
    emotions = relationship("Emotion", back_populates="entry", cascade="all, delete-orphan")

class Emotion(Base):
    __tablename__ = "emotions"

    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(Integer, ForeignKey("entries.id"), nullable=False)
    emotion_type = Column(String, nullable=False)  # happy, sad, angry, neutral, etc.
    confidence_score = Column(Float, nullable=False)  # 0.0 to 1.0
    analyzed_text = Column(Text)  # 분석된 텍스트 부분
    model_version = Column(String, default="v1.0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    entry = relationship("Entry", back_populates="emotions")