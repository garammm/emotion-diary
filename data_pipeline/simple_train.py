"""
간단한 KoBERT 모델 학습 스크립트 (빠른 테스트용)
"""

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset
import numpy as np
from pathlib import Path

class SimpleEmotionDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(self.labels[idx], dtype=torch.long)
        }

def main():
    print("🚀 간단한 KoBERT 감정 분류 모델 학습 시작!")
    
    # 라벨링된 데이터 로드 (현재 디렉토리 기준)
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'data', 'labeled', 'auto_labeled_data.csv')
    df = pd.read_csv(data_path)
    print(f'📊 학습 데이터: {len(df)}개')
    
    # 감정 라벨 매핑
    emotion_to_label = {
        "중립": 0, "기쁨": 1, "슬픔": 2, "분노": 3,
        "두려움": 4, "놀라움": 5, "혐오": 6
    }
    
    # 데이터 준비
    texts = df['text'].tolist()
    labels = [emotion_to_label.get(emotion, 0) for emotion in df['emotion']]
    
    # 텍스트 길이 제한 (빠른 학습을 위해)
    texts = [text[:200] for text in texts]
    
    print(f"📝 데이터 준비 완료: {len(texts)}개 텍스트")
    
    # 모델과 토크나이저 로드 (더 작은 모델 사용)
    model_name = "klue/bert-base"
    print(f"🤖 모델 로딩: {model_name}")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=7)
    
    # Train/Test 분리
    train_texts, test_texts, train_labels, test_labels = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )
    
    # 데이터셋 생성
    train_dataset = SimpleEmotionDataset(train_texts, train_labels, tokenizer)
    test_dataset = SimpleEmotionDataset(test_texts, test_labels, tokenizer)
    
    print(f"🏋️ 학습 데이터: {len(train_dataset)}개, 테스트 데이터: {len(test_dataset)}개")
    
    # 학습 설정 (빠른 학습을 위해 간소화)
    training_args = TrainingArguments(
        output_dir='../models/kobert_emotion_simple',
        num_train_epochs=2,  # 빠른 테스트를 위해 2 에포크만
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=100,
        weight_decay=0.01,
        logging_dir='../models/kobert_emotion_simple/logs',
        logging_steps=10,
        eval_strategy="steps",  # evaluation_strategy 대신 eval_strategy 사용
        eval_steps=50,
        save_strategy="epoch",
        load_best_model_at_end=True
    )
    
    # 트레이너 생성
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        tokenizer=tokenizer
    )
    
    print("🎯 모델 학습 시작...")
    
    # 학습 실행
    trainer.train()
    
    # 모델 저장
    output_dir = Path('../models/kobert_emotion_simple')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    trainer.save_model()
    tokenizer.save_pretrained(output_dir)
    
    print(f"✅ 모델 학습 및 저장 완료: {output_dir}")
    print("🎉 KoBERT 감정 분류 모델이 준비되었습니다!")

if __name__ == "__main__":
    main()