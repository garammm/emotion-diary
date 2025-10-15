from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from loguru import logger

from ..database import get_db
from ..models import Entry, User
from ..schemas import Entry as EntrySchema, EntryCreate, EntryUpdate, EntryWithEmotions
from ..routers.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=EntrySchema)
async def create_entry(
    entry: EntryCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_entry = Entry(
        **entry.dict(),
        user_id=current_user.id
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    
    logger.info(f"User {current_user.username} created a new entry: {db_entry.id}")
    return db_entry

@router.get("/", response_model=List[EntrySchema])
async def read_entries(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entries = db.query(Entry).filter(Entry.user_id == current_user.id).offset(skip).limit(limit).all()
    return entries

@router.get("/{entry_id}", response_model=EntryWithEmotions)
async def read_entry(
    entry_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entry = db.query(Entry).filter(Entry.id == entry_id, Entry.user_id == current_user.id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry

@router.put("/{entry_id}", response_model=EntrySchema)
async def update_entry(
    entry_id: int, 
    entry_update: EntryUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entry = db.query(Entry).filter(Entry.id == entry_id, Entry.user_id == current_user.id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    update_data = entry_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(entry, field, value)
    
    db.commit()
    db.refresh(entry)
    
    logger.info(f"User {current_user.username} updated entry: {entry_id}")
    return entry

@router.delete("/{entry_id}")
async def delete_entry(
    entry_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entry = db.query(Entry).filter(Entry.id == entry_id, Entry.user_id == current_user.id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    db.delete(entry)
    db.commit()
    
    logger.info(f"User {current_user.username} deleted entry: {entry_id}")
    return {"message": "Entry deleted successfully"}

@router.get("/{entry_id}/analyze", response_model=EntryWithEmotions)
async def analyze_entry_emotions(
    entry_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyze emotions for a specific entry"""
    entry = db.query(Entry).filter(Entry.id == entry_id, Entry.user_id == current_user.id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    # Import emotion service here to avoid circular imports
    from ..services.kobert_emotion_service import analyze_emotion
    from ..models import Emotion
    
    # Analyze emotion
    emotion_result = analyze_emotion(entry.content)
    
    # Save emotion analysis
    db_emotion = Emotion(
        entry_id=entry.id,
        emotion_type=emotion_result["emotion_type"],
        confidence_score=emotion_result["confidence_score"],
        analyzed_text=entry.content,
        model_version="v1.0"
    )
    
    db.add(db_emotion)
    db.commit()
    db.refresh(db_emotion)
    
    # Refresh entry to include new emotion
    db.refresh(entry)
    
    logger.info(f"Analyzed emotions for entry {entry_id}: {emotion_result['emotion_type']}")
    return entry