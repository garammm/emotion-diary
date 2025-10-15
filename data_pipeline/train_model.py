"""
KoBERT 모델 학습 스크립트
"""

from src.model_training import KoBERTTrainer, DataPreprocessor
import pandas as pd
import os
from pathlib import Path

def main():
    # 라벨링된 데이터 로드
    df = pd.read_csv('data/labeled/auto_labeled_data.csv')
    print(f'학습 데이터: {len(df)}개')
    print(f'감정 분포:')
    print(df['emotion'].value_counts())
    
    # 데이터 전처리
    preprocessor = DataPreprocessor()
    
    # 감정 라벨을 숫자로 변환
    emotion_to_label = {
        "중립": 0, "기쁨": 1, "슬픔": 2, "분노": 3,
        "두려움": 4, "놀라움": 5, "혐오": 6
    }
    
    # 데이터 준비
    texts = df['text'].tolist()
    labels = [emotion_to_label.get(emotion, 0) for emotion in df['emotion']]
    
    print(f'텍스트 {len(texts)}개, 라벨 {len(labels)}개 준비 완료')
    
    # 학습용 DataFrame 생성
    train_df = pd.DataFrame({
        'text': texts,
        'label': labels
    })
    
    # 모델 트레이너 초기화
    trainer = KoBERTTrainer()
    trainer.setup_model()
    
    # 데이터셋 준비 (train/val 분리)
    train_dataset, val_dataset, test_dataset, test_df = trainer.prepare_datasets(train_df)
    print(f'Train: {len(train_dataset)}, Val: {len(val_dataset)}, Test: {len(test_dataset)}')
    
    # 모델 저장 디렉토리 생성
    output_dir = Path('../models/kobert_emotion')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 학습 실행
    trainer.train_model(train_dataset, val_dataset, output_dir='../models/kobert_emotion')
    print('KoBERT 모델 학습 완료!')

if __name__ == "__main__":
    main()