import pytest
from app.services.emotion_service import analyze_emotion, EmotionAnalyzer

def test_analyze_emotion_happy():
    result = analyze_emotion("오늘 정말 기쁘고 행복한 하루였어요!")
    
    assert "emotion_type" in result
    assert "confidence_score" in result
    assert "all_emotions" in result
    
    assert result["emotion_type"] == "happy"
    assert isinstance(result["confidence_score"], float)
    assert 0 <= result["confidence_score"] <= 1

def test_analyze_emotion_sad():
    result = analyze_emotion("너무 슬프고 힘든 하루였습니다. 우울해요.")
    
    assert result["emotion_type"] == "sad"
    assert isinstance(result["confidence_score"], float)

def test_analyze_emotion_empty_text():
    result = analyze_emotion("")
    
    assert result["emotion_type"] == "neutral"
    assert result["confidence_score"] == 0.5

def test_analyze_emotion_neutral():
    result = analyze_emotion("그냥 평범한 하루였어요.")
    
    assert "emotion_type" in result
    assert isinstance(result["confidence_score"], float)

def test_emotion_analyzer_singleton():
    analyzer1 = EmotionAnalyzer()
    analyzer2 = EmotionAnalyzer()
    
    # Different instances but same behavior
    result1 = analyzer1.analyze("기쁜 하루")
    result2 = analyzer2.analyze("기쁜 하루")
    
    assert result1["emotion_type"] == result2["emotion_type"]

def test_emotion_analyzer_preprocess():
    analyzer = EmotionAnalyzer()
    
    text = "안녕하세요!!! 좋은@#$ 하루 되세요..."
    processed = analyzer.preprocess_text(text)
    
    # Should remove special characters and normalize
    assert "!" not in processed
    assert "@" not in processed
    assert "#" not in processed