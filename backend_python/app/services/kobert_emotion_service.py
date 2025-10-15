"""
학습된 KoBERT 모델을 사용한 감정 분석 서비스
기존의 규칙 기반 분석기를 대체
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from typing import Dict, Any, Optional
from loguru import logger
import os
from pathlib import Path

class KoBERTEmotionAnalyzer:
    """KoBERT 기반 감정 분석기"""
    
    EMOTIONS = {
        0: "중립",
        1: "기쁨", 
        2: "슬픔",
        3: "분노",
        4: "두려움",
        5: "놀라움",
        6: "혐오"
    }
    
    def __init__(self, model_path: str = "models/kobert_emotion"):
        self.model_path = model_path
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # 모델 로드 시도
        if self._model_exists():
            self._load_model()
        else:
            logger.warning(f"KoBERT 모델을 찾을 수 없습니다: {model_path}")
            logger.info("규칙 기반 분석기를 사용합니다.")
    
    def _model_exists(self) -> bool:
        """모델 파일 존재 확인"""
        model_path = Path(self.model_path)
        return (model_path / "pytorch_model.bin").exists() and (model_path / "tokenizer.json").exists()
    
    def _load_model(self):
        """모델과 토크나이저 로드"""
        try:
            logger.info(f"KoBERT 모델 로딩: {self.model_path}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"KoBERT 모델 로딩 완료 (Device: {self.device})")
            
        except Exception as e:
            logger.error(f"KoBERT 모델 로딩 실패: {e}")
            self.tokenizer = None
            self.model = None
    
    def predict(self, text: str) -> Dict[str, Any]:
        """감정 예측"""
        if not text or not text.strip():
            return {
                "emotion_type": "중립",
                "confidence_score": 0.5,
                "all_emotions": {"중립": 0.5}
            }
        
        # KoBERT 모델이 로드되어 있으면 사용
        if self.model is not None and self.tokenizer is not None:
            return self._predict_with_kobert(text)
        else:
            # fallback: 규칙 기반 분석
            return self._predict_with_rules(text)
    
    def _predict_with_kobert(self, text: str) -> Dict[str, Any]:
        """KoBERT 모델로 예측"""
        try:
            # 토크나이징
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=512
            )
            
            # GPU로 이동
            inputs = {key: value.to(self.device) for key, value in inputs.items()}
            
            # 예측
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                predictions = predictions.cpu().numpy()[0]
            
            # 결과 파싱
            emotion_probs = {self.EMOTIONS[i]: float(predictions[i]) for i in range(len(predictions))}
            
            # 가장 높은 확률의 감정
            best_emotion_idx = np.argmax(predictions)
            best_emotion = self.EMOTIONS[best_emotion_idx]
            confidence = float(predictions[best_emotion_idx])
            
            return {
                "emotion_type": best_emotion,
                "confidence_score": confidence,
                "all_emotions": emotion_probs,
                "model_type": "kobert"
            }
            
        except Exception as e:
            logger.error(f"KoBERT 예측 오류: {e}")
            # fallback to rule-based
            return self._predict_with_rules(text)
    
    def _predict_with_rules(self, text: str) -> Dict[str, Any]:
        """규칙 기반 예측 (fallback)"""
        emotion_keywords = {
            "기쁨": ["기쁘", "행복", "좋", "웃", "즐거", "신나", "만족", "성공", "사랑", "고마워"],
            "슬픔": ["슬프", "우울", "힘들", "아프", "괴로", "눈물", "울", "실망", "좌절", "외로"],
            "분노": ["화", "짜증", "분노", "열받", "빡치", "싫", "미워", "증오", "억울", "불만"],
            "두려움": ["무서", "두려", "걱정", "불안", "긴장", "떨", "공포", "위험", "조심"],
            "놀라움": ["놀라", "깜짝", "의외", "갑자기", "예상외", "충격", "발견", "처음"],
            "혐오": ["더러", "역겨", "싫", "혐오", "구역", "토", "못참", "지겨"],
            "중립": ["그냥", "평범", "보통", "일반", "무난", "평소"]
        }
        
        emotion_scores = {}
        text_lower = text.lower()
        
        for emotion, keywords in emotion_keywords.items():
            score = sum(text_lower.count(keyword) for keyword in keywords)
            emotion_scores[emotion] = score
        
        # 정규화
        total_score = sum(emotion_scores.values())
        if total_score == 0:
            return {
                "emotion_type": "중립",
                "confidence_score": 0.5,
                "all_emotions": {"중립": 0.5},
                "model_type": "rule_based"
            }
        
        emotion_probs = {k: v/total_score for k, v in emotion_scores.items()}
        best_emotion = max(emotion_probs, key=emotion_probs.get)
        confidence = emotion_probs[best_emotion]
        
        return {
            "emotion_type": best_emotion,
            "confidence_score": confidence,
            "all_emotions": emotion_probs,
            "model_type": "rule_based"
        }

# 전역 분석기 인스턴스
_kobert_analyzer = None

def get_kobert_analyzer():
    """KoBERT 분석기 싱글톤 인스턴스 반환"""
    global _kobert_analyzer
    if _kobert_analyzer is None:
        _kobert_analyzer = KoBERTEmotionAnalyzer()
        logger.info("KoBERT 감정 분석기 초기화 완료")
    return _kobert_analyzer

def analyze_emotion(text: str) -> Dict[str, Any]:
    """감정 분석 함수 (업데이트된 버전)"""
    try:
        analyzer = get_kobert_analyzer()
        result = analyzer.predict(text)
        logger.debug(f"감정 분석 결과: {result}")
        return result
    except Exception as e:
        logger.error(f"감정 분석 오류: {str(e)}")
        # 오류 시 기본값 반환
        return {
            "emotion_type": "중립",
            "confidence_score": 0.5,
            "all_emotions": {"중립": 0.5},
            "model_type": "error_fallback"
        }

# 모델 로드 확인 함수
def check_model_status():
    """모델 상태 확인"""
    analyzer = get_kobert_analyzer()
    return {
        "model_loaded": analyzer.model is not None,
        "model_path": analyzer.model_path,
        "device": str(analyzer.device),
        "available_emotions": list(analyzer.EMOTIONS.values())
    }