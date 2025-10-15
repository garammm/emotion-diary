"""
데이터 전처리 및 KoBERT 모델 학습 파이프라인
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    TrainingArguments, 
    Trainer,
    EarlyStoppingCallback
)
import sqlite3
from pathlib import Path
import json
import re
from typing import List, Dict, Tuple
from loguru import logger
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class EmotionDataset(Dataset):
    """감정 분석용 데이터셋"""
    
    def __init__(self, texts: List[str], labels: List[int], tokenizer, max_length: int = 512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = int(self.labels[idx])
        
        # 토크나이징
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
            'labels': torch.tensor(label, dtype=torch.long)
        }

class DataPreprocessor:
    """데이터 전처리 클래스"""
    
    def __init__(self):
        self.emotion_mapping = {
            0: "중립", 1: "기쁨", 2: "슬픔", 3: "분노", 
            4: "두려움", 5: "놀라움", 6: "혐오"
        }
    
    def clean_text(self, text: str) -> str:
        """텍스트 정제"""
        if pd.isna(text) or not text:
            return ""
        
        text = str(text)
        
        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', text)
        
        # URL 제거
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # 이메일 제거
        text = re.sub(r'\S+@\S+', '', text)
        
        # 특수 문자 정규화 (한글, 영문, 숫자, 기본 문장부호만 유지)
        text = re.sub(r'[^가-힣a-zA-Z0-9\s.,!?]', ' ', text)
        
        # 연속된 공백 제거
        text = re.sub(r'\s+', ' ', text)
        
        # 너무 짧거나 긴 텍스트 필터링
        if len(text.strip()) < 10 or len(text.strip()) > 1000:
            return ""
        
        return text.strip()
    
    def load_labeled_data(self, db_path: str = "data/labels.db") -> pd.DataFrame:
        """라벨링된 데이터 로드"""
        conn = sqlite3.connect(db_path)
        
        query = '''
            SELECT text, 
                   COALESCE(human_label, auto_label) as label,
                   source,
                   is_verified
            FROM labeled_data 
            WHERE (human_label IS NOT NULL OR auto_label IS NOT NULL)
            AND text IS NOT NULL
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        logger.info(f"로드된 데이터: {len(df)}개")
        return df
    
    def preprocess_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """데이터셋 전처리"""
        logger.info("데이터 전처리 시작...")
        
        # 텍스트 정제
        df['cleaned_text'] = df['text'].apply(self.clean_text)
        
        # 빈 텍스트 제거
        df = df[df['cleaned_text'].str.len() > 0].copy()
        
        # 라벨 검증 (0-6 범위)
        df = df[df['label'].between(0, 6)].copy()
        
        # 중복 제거 (텍스트 기준)
        df = df.drop_duplicates(subset=['cleaned_text']).copy()
        
        logger.info(f"전처리 완료: {len(df)}개 데이터")
        
        return df
    
    def analyze_dataset(self, df: pd.DataFrame) -> Dict:
        """데이터셋 분석"""
        analysis = {
            'total_samples': len(df),
            'label_distribution': df['label'].value_counts().to_dict(),
            'text_length_stats': {
                'mean': df['cleaned_text'].str.len().mean(),
                'std': df['cleaned_text'].str.len().std(),
                'min': df['cleaned_text'].str.len().min(),
                'max': df['cleaned_text'].str.len().max()
            },
            'source_distribution': df['source'].value_counts().to_dict()
        }
        
        # 클래스 불균형 체크
        label_counts = df['label'].value_counts()
        analysis['class_imbalance_ratio'] = label_counts.max() / label_counts.min()
        
        return analysis
    
    def create_balanced_dataset(self, df: pd.DataFrame, min_samples: int = 100) -> pd.DataFrame:
        """클래스 균형 맞추기"""
        balanced_dfs = []
        
        for label in df['label'].unique():
            label_df = df[df['label'] == label].copy()
            
            if len(label_df) < min_samples:
                # 언더샘플링된 클래스는 복제로 증강
                multiplier = min_samples // len(label_df) + 1
                label_df = pd.concat([label_df] * multiplier, ignore_index=True)
                label_df = label_df.sample(n=min_samples, random_state=42)
            else:
                # 오버샘플링된 클래스는 다운샘플링
                label_df = label_df.sample(n=min(len(label_df), min_samples * 3), random_state=42)
            
            balanced_dfs.append(label_df)
        
        balanced_df = pd.concat(balanced_dfs, ignore_index=True)
        balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        logger.info(f"균형 조정 완료: {len(balanced_df)}개 데이터")
        return balanced_df

class KoBERTTrainer:
    """KoBERT 모델 파인튜닝 클래스"""
    
    def __init__(self, model_name: str = "klue/bert-base"):
        self.model_name = model_name
        self.num_labels = 7  # 감정 라벨 수
        self.tokenizer = None
        self.model = None
    
    def setup_model(self):
        """모델 및 토크나이저 초기화"""
        logger.info(f"모델 로딩: {self.model_name}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=self.num_labels
        )
        
        logger.info("모델 로딩 완료")
    
    def prepare_datasets(self, df: pd.DataFrame, test_size: float = 0.2, val_size: float = 0.1):
        """학습/검증/테스트 데이터셋 준비"""
        # 먼저 train/test 분리
        train_df, test_df = train_test_split(
            df, 
            test_size=test_size, 
            random_state=42,
            stratify=df['label']
        )
        
        # train에서 validation 분리
        train_df, val_df = train_test_split(
            train_df,
            test_size=val_size,
            random_state=42,
            stratify=train_df['label']
        )
        
        # 데이터셋 생성
        train_dataset = EmotionDataset(
            train_df['cleaned_text'].tolist(),
            train_df['label'].tolist(),
            self.tokenizer
        )
        
        val_dataset = EmotionDataset(
            val_df['cleaned_text'].tolist(),
            val_df['label'].tolist(),
            self.tokenizer
        )
        
        test_dataset = EmotionDataset(
            test_df['cleaned_text'].tolist(),
            test_df['label'].tolist(),
            self.tokenizer
        )
        
        logger.info(f"데이터셋 준비 완료 - Train: {len(train_dataset)}, Val: {len(val_dataset)}, Test: {len(test_dataset)}")
        
        return train_dataset, val_dataset, test_dataset, test_df
    
    def train_model(self, train_dataset, val_dataset, output_dir: str = "models/kobert_emotion"):
        """모델 학습"""
        logger.info("모델 학습 시작...")
        
        # 학습 설정
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=5,
            per_device_train_batch_size=16,
            per_device_eval_batch_size=16,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir=f'{output_dir}/logs',
            logging_steps=100,
            evaluation_strategy="steps",
            eval_steps=500,
            save_strategy="steps",
            save_steps=500,
            save_total_limit=3,
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            greater_is_better=False,
            dataloader_num_workers=4,
            fp16=torch.cuda.is_available(),
            report_to=None  # wandb 사용 안 함
        )
        
        # 트레이너 생성
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
        )
        
        # 학습 실행
        trainer.train()
        
        # 모델 저장
        trainer.save_model()
        self.tokenizer.save_pretrained(output_dir)
        
        logger.info(f"모델 학습 완료. 저장 위치: {output_dir}")
        
        return trainer
    
    def evaluate_model(self, trainer, test_dataset, test_df: pd.DataFrame):
        """모델 평가"""
        logger.info("모델 평가 시작...")
        
        # 예측
        predictions = trainer.predict(test_dataset)
        y_pred = np.argmax(predictions.predictions, axis=1)
        y_true = test_df['label'].values
        
        # 분류 리포트
        report = classification_report(
            y_true, y_pred,
            target_names=[f"Class_{i}" for i in range(self.num_labels)],
            output_dict=True
        )
        
        # 혼동 행렬
        cm = confusion_matrix(y_true, y_pred)
        
        # 시각화
        self.plot_evaluation_results(cm, report)
        
        logger.info("모델 평가 완료")
        
        return report, cm
    
    def plot_evaluation_results(self, confusion_matrix, classification_report):
        """평가 결과 시각화"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # 혼동 행렬
        emotion_labels = ["중립", "기쁨", "슬픔", "분노", "두려움", "놀라움", "혐오"]
        sns.heatmap(confusion_matrix, annot=True, fmt='d', cmap='Blues',
                   xticklabels=emotion_labels, yticklabels=emotion_labels, ax=axes[0])
        axes[0].set_title('Confusion Matrix')
        axes[0].set_xlabel('Predicted')
        axes[0].set_ylabel('Actual')
        
        # F1 스코어
        f1_scores = [classification_report[f"Class_{i}"]["f1-score"] for i in range(7)]
        axes[1].bar(emotion_labels, f1_scores)
        axes[1].set_title('F1 Scores by Emotion')
        axes[1].set_ylabel('F1 Score')
        axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(f'evaluation_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()

def main():
    """메인 실행 함수"""
    # 1. 데이터 전처리
    preprocessor = DataPreprocessor()
    
    # 라벨링된 데이터 로드
    df = preprocessor.load_labeled_data()
    
    if df.empty:
        logger.error("라벨링된 데이터가 없습니다. 먼저 데이터를 수집하고 라벨링하세요.")
        return
    
    # 데이터 전처리
    df = preprocessor.preprocess_dataset(df)
    
    # 데이터셋 분석
    analysis = preprocessor.analyze_dataset(df)
    logger.info(f"데이터셋 분석 결과: {json.dumps(analysis, indent=2, ensure_ascii=False)}")
    
    # 클래스 균형 조정
    df = preprocessor.create_balanced_dataset(df)
    
    # 2. 모델 학습
    trainer = KoBERTTrainer()
    trainer.setup_model()
    
    # 데이터셋 분리
    train_dataset, val_dataset, test_dataset, test_df = trainer.prepare_datasets(df)
    
    # 모델 학습
    model_trainer = trainer.train_model(train_dataset, val_dataset)
    
    # 3. 모델 평가
    report, cm = trainer.evaluate_model(model_trainer, test_dataset, test_df)
    
    # 결과 저장
    results = {
        'dataset_analysis': analysis,
        'classification_report': report,
        'confusion_matrix': cm.tolist(),
        'timestamp': datetime.now().isoformat()
    }
    
    with open(f'training_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    logger.info("학습 완료!")

if __name__ == "__main__":
    main()