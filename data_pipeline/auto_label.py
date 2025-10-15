"""
자동 라벨링 스크립트
"""

import pandas as pd
import re
from pathlib import Path

class SimpleEmotionLabeler:
    """간단한 규칙 기반 감정 라벨러"""
    
    EMOTION_KEYWORDS = {
        "기쁨": ["기쁘", "행복", "좋", "웃", "즐거", "신나", "만족", "성공", "사랑", "고마워", "최고", "대단", "축하", "좋아"],
        "슬픔": ["슬프", "우울", "힘들", "아프", "괴로", "눈물", "울", "실망", "좌절", "외로", "그리워", "죽고", "마음아파"],
        "분노": ["화", "짜증", "분노", "열받", "빡치", "싫", "미워", "증오", "억울", "불만", "욕", "진짜", "개", "씨"],
        "두려움": ["무서", "두려", "걱정", "불안", "긴장", "떨", "공포", "위험", "조심", "피하", "겁", "불안"],
        "놀라움": ["놀라", "깜짝", "의외", "갑자기", "예상외", "충격", "발견", "처음", "새로", "대박", "와"],
        "혐오": ["더러", "역겨", "싫", "혐오", "구역", "토", "못참", "지겨", "답답", "짜증", "역겨워"],
        "중립": ["그냥", "평범", "보통", "일반", "무난", "평소", "항상", "매일", "소식", "안내"]
    }
    
    def predict_emotion_rule_based(self, text: str) -> str:
        """규칙 기반 감정 예측"""
        if not text:
            return "중립"
        
        text = text.lower()
        emotion_scores = {}
        
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            score = sum(text.count(keyword) for keyword in keywords)
            emotion_scores[emotion] = score
        
        # 가장 높은 점수의 감정 반환
        if max(emotion_scores.values()) == 0:
            return "중립"
        
        return max(emotion_scores, key=emotion_scores.get)

def main():
    # 라벨러 인스턴스 생성
    labeler = SimpleEmotionLabeler()
    
    # 수집된 데이터 로드
    df = pd.read_csv('data/raw/crawled_data_20251015_165830.csv')
    print(f'로드된 데이터: {len(df)}개')
    
    # 자동 라벨링 실행
    labeled_data = []
    for idx, row in df.iterrows():
        emotion = labeler.predict_emotion_rule_based(row['text'])
        labeled_data.append({
            'text': row['text'][:500],  # 텍스트 길이 제한
            'emotion': emotion,
            'source': row['source'],
            'confidence': 0.6  # 규칙 기반이므로 낮은 신뢰도
        })
        if idx % 50 == 0:
            print(f'진행: {idx+1}/{len(df)}')
    
    # 라벨링된 데이터 저장
    labeled_df = pd.DataFrame(labeled_data)
    labeled_df.to_csv('data/labeled/auto_labeled_data.csv', index=False, encoding='utf-8-sig')
    print(f'자동 라벨링 완료: {len(labeled_df)}개 데이터 저장')
    print(f'감정 분포:')
    print(labeled_df['emotion'].value_counts())

if __name__ == "__main__":
    main()