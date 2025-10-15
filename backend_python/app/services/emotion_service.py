import re
from typing import Dict, Any
from loguru import logger
import numpy as np

class EmotionAnalyzer:
    def __init__(self):
        """
        감정 분석을 위한 간단한 규칙 기반 분석기
        실제 운영환경에서는 transformers 라이브러리의 사전 훈련된 모델을 사용할 수 있습니다.
        """
        # 감정별 키워드 사전
        self.emotion_keywords = {
            "happy": [
                "기쁘", "행복", "좋", "웃", "즐거", "신나", "만족", "성공", "달성", "완성",
                "사랑", "고마", "감사", "축하", "재미", "유쾌", "흥미", "놀라", "환상적",
                "멋지", "훌륭", "완벽", "최고", "대단", "놀랍"
            ],
            "sad": [
                "슬프", "우울", "힘들", "아프", "괴로", "눈물", "울", "실망", "좌절", "포기",
                "외로", "고독", "그리", "보고싶", "안타까", "미안", "후회", "아쉽", "절망",
                "침울", "막막", "답답", "허무", "쓸쓸"
            ],
            "angry": [
                "화", "짜증", "분노", "열받", "빡치", "멘탈", "스트레스", "싫", "미워", "증오",
                "억울", "답답", "불만", "항의", "반대", "거부", "저항", "비판", "욕설",
                "폭발", "터지", "끓", "불쾌", "혐오"
            ],
            "fear": [
                "무서", "두려", "걱정", "불안", "긴장", "떨", "심장", "공포", "위험", "위기",
                "조심", "주의", "경계", "피하", "숨", "도망", "망설", "고민", "걱정",
                "불확실", "모르겠", "확신", "의심"
            ],
            "surprise": [
                "놀라", "깜짝", "의외", "갑자기", "예상외", "뜨밖", "충격", "소식", "발견",
                "알았", "깨달", "느낀", "경험", "처음", "새로", "달라", "변화", "다른"
            ],
            "neutral": [
                "그냥", "평범", "보통", "일반", "똑같", "비슷", "그럭저럭", "나쁘지않", "괜찮",
                "할만", "적당", "무난", "평소", "항상", "언제나", "매일", "계속", "반복"
            ]
        }
        
    def preprocess_text(self, text: str) -> str:
        """텍스트 전처리"""
        # 특수문자 제거 (한글, 영문, 숫자, 공백만 유지)
        text = re.sub(r'[^가-힣a-zA-Z0-9\s]', '', text)
        # 연속된 공백을 하나로
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()
    
    def calculate_emotion_scores(self, text: str) -> Dict[str, float]:
        """감정별 점수 계산"""
        preprocessed_text = self.preprocess_text(text)
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            for keyword in keywords:
                # 키워드가 텍스트에 포함된 횟수
                count = preprocessed_text.count(keyword)
                score += count
            
            # 텍스트 길이로 정규화
            text_length = len(preprocessed_text.split())
            if text_length > 0:
                emotion_scores[emotion] = score / text_length
            else:
                emotion_scores[emotion] = 0
        
        return emotion_scores
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """감정 분석 수행"""
        if not text or not text.strip():
            return {
                "emotion_type": "neutral",
                "confidence_score": 0.5,
                "all_emotions": {"neutral": 0.5}
            }
        
        emotion_scores = self.calculate_emotion_scores(text)
        
        # 가장 높은 점수의 감정 찾기
        max_emotion = max(emotion_scores, key=emotion_scores.get)
        max_score = emotion_scores[max_emotion]
        
        # 모든 점수가 0이면 neutral
        if max_score == 0:
            return {
                "emotion_type": "neutral",
                "confidence_score": 0.5,
                "all_emotions": emotion_scores
            }
        
        # 신뢰도 점수 계산 (0.5 ~ 1.0 범위로)
        total_score = sum(emotion_scores.values())
        if total_score > 0:
            confidence = 0.5 + (max_score / total_score) * 0.5
        else:
            confidence = 0.5
        
        return {
            "emotion_type": max_emotion,
            "confidence_score": round(confidence, 3),
            "all_emotions": {k: round(v, 3) for k, v in emotion_scores.items()}
        }

# 전역 분석기 인스턴스
_emotion_analyzer = None

def get_emotion_analyzer():
    """감정 분석기 싱글톤 인스턴스 반환"""
    global _emotion_analyzer
    if _emotion_analyzer is None:
        _emotion_analyzer = EmotionAnalyzer()
        logger.info("Emotion analyzer initialized")
    return _emotion_analyzer

def analyze_emotion(text: str) -> Dict[str, Any]:
    """감정 분석 함수"""
    try:
        analyzer = get_emotion_analyzer()
        result = analyzer.analyze(text)
        logger.debug(f"Emotion analysis result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in emotion analysis: {str(e)}")
        # 오류 시 기본값 반환
        return {
            "emotion_type": "neutral",
            "confidence_score": 0.5,
            "all_emotions": {"neutral": 0.5, "error": True}
        }