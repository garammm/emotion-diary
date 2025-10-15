from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from loguru import logger

from ..database import get_db
from ..models import Emotion, User
from ..schemas import Emotion as EmotionSchema, EmotionAnalysisRequest, EmotionAnalysisResponse
from ..routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[EmotionSchema])
async def read_emotions(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get emotions for entries owned by current user
    emotions = (
        db.query(Emotion)
        .join(Emotion.entry)
        .filter(Emotion.entry.has(user_id=current_user.id))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return emotions

@router.get("/{emotion_id}", response_model=EmotionSchema)
async def read_emotion(
    emotion_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    emotion = (
        db.query(Emotion)
        .join(Emotion.entry)
        .filter(
            Emotion.id == emotion_id,
            Emotion.entry.has(user_id=current_user.id)
        )
        .first()
    )
    if emotion is None:
        raise HTTPException(status_code=404, detail="Emotion not found")
    return emotion

@router.post("/analyze", response_model=EmotionAnalysisResponse)
async def analyze_text_emotion(
    request: EmotionAnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    """Analyze emotion for arbitrary text without saving to database"""
    from ..services.kobert_emotion_service import analyze_emotion
    
    result = analyze_emotion(request.text)
    
    logger.info(f"User {current_user.username} analyzed text emotion: {result['emotion_type']}")
    
    return EmotionAnalysisResponse(
        emotion_type=result["emotion_type"],
        confidence_score=result["confidence_score"],
        all_emotions=result["all_emotions"]
    )

@router.post("/test", response_model=EmotionAnalysisResponse)
async def test_emotion_analysis(request: EmotionAnalysisRequest):
    """공개 테스트용 감정 분석 엔드포인트 (인증 불필요)"""
    from ..services.kobert_emotion_service import analyze_emotion
    
    try:
        result = analyze_emotion(request.text)
        logger.info(f"Test emotion analysis: {result['emotion_type']}")
        
        return EmotionAnalysisResponse(
            emotion_type=result["emotion_type"],
            confidence_score=result["confidence_score"],
            all_emotions=result["all_emotions"]
        )
    except Exception as e:
        logger.error(f"Test emotion analysis error: {e}")
        raise HTTPException(status_code=500, detail="감정 분석 중 오류가 발생했습니다.")

@router.delete("/{emotion_id}")
async def delete_emotion(
    emotion_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    emotion = (
        db.query(Emotion)
        .join(Emotion.entry)
        .filter(
            Emotion.id == emotion_id,
            Emotion.entry.has(user_id=current_user.id)
        )
        .first()
    )
    if emotion is None:
        raise HTTPException(status_code=404, detail="Emotion not found")
    
    db.delete(emotion)
    db.commit()
    
    logger.info(f"User {current_user.username} deleted emotion: {emotion_id}")
    return {"message": "Emotion deleted successfully"}