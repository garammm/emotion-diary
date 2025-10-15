from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_active: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Entry schemas
class EntryBase(BaseModel):
    title: str
    content: str
    date: datetime

class EntryCreate(EntryBase):
    pass

class EntryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    date: Optional[datetime] = None

class Entry(EntryBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Emotion schemas
class EmotionBase(BaseModel):
    emotion_type: str
    confidence_score: float
    analyzed_text: Optional[str] = None
    model_version: str = "v1.0"

class EmotionCreate(EmotionBase):
    entry_id: int

class Emotion(EmotionBase):
    id: int
    entry_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Response schemas with relationships
class EntryWithEmotions(Entry):
    emotions: List[Emotion] = []

class UserWithEntries(User):
    entries: List[Entry] = []

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Emotion analysis request
class EmotionAnalysisRequest(BaseModel):
    text: str

class EmotionAnalysisResponse(BaseModel):
    emotion_type: str
    confidence_score: float
    all_emotions: dict