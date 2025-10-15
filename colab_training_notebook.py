"""
Google Colab에서 KoBERT 감정 분류 모델 학습
이 코드를 Colab에 복사해서 사용하세요.
"""

# ===== Google Colab 노트북 코드 =====

# 1. 필요한 패키지 설치
!pip install transformers torch datasets scikit-learn pandas numpy

# 2. Google Drive 마운트 (모델 저장을 위해)
from google.colab import drive
drive.mount('/content/drive')

# 3. 라이브러리 import
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import TrainingArguments, Trainer
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset
import numpy as np
from datetime import datetime

# 4. 감정 데이터셋 클래스
class EmotionDataset(Dataset):
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

# 5. 샘플 데이터 준비 (실제로는 업로드한 CSV 사용)
# CSV 파일을 Colab에 업로드하고 경로 수정
sample_data = {
    'text': [
        '오늘 정말 기뻤어!',
        '너무 슬프다...',
        '화가 나서 미치겠어',
        '무서워서 떨려',
        '와! 놀랍다!',
        '정말 역겨워',
        '그냥 평범한 하루였다'
    ] * 50,  # 350개 샘플
    'emotion': [
        '기쁨', '슬픔', '분노', '두려움', 
        '놀라움', '혐오', '중립'
    ] * 50
}

df = pd.DataFrame(sample_data)
print(f"데이터 크기: {len(df)}")
print(f"감정 분포:\n{df['emotion'].value_counts()}")

# 6. 감정 라벨 매핑
emotion_to_label = {
    "중립": 0, "기쁨": 1, "슬픔": 2, "분노": 3,
    "두려움": 4, "놀라움": 5, "혐오": 6
}

df['label'] = df['emotion'].map(emotion_to_label)

# 7. 모델과 토크나이저 로드
model_name = "klue/bert-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=7)

# 8. 데이터 분할
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df['text'].tolist(), 
    df['label'].tolist(), 
    test_size=0.2, 
    random_state=42,
    stratify=df['label']
)

# 9. 데이터셋 생성
train_dataset = EmotionDataset(train_texts, train_labels, tokenizer)
val_dataset = EmotionDataset(val_texts, val_labels, tokenizer)

print(f"학습 데이터: {len(train_dataset)}")
print(f"검증 데이터: {len(val_dataset)}")

# 10. 학습 설정
training_args = TrainingArguments(
    output_dir='/content/drive/MyDrive/kobert_emotion_results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='/content/drive/MyDrive/kobert_emotion_logs',
    logging_steps=50,
    evaluation_strategy="steps",
    eval_steps=100,
    save_strategy="steps",
    save_steps=100,
    save_total_limit=2,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    report_to=None,
    dataloader_num_workers=2,
    fp16=True  # GPU 가속
)

# 11. 트레이너 설정
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer
)

# 12. 학습 실행
print("🚀 KoBERT 감정 분류 모델 학습 시작!")
trainer.train()

# 13. 최종 모델 저장
save_path = "/content/drive/MyDrive/kobert_emotion_final"
trainer.save_model(save_path)
tokenizer.save_pretrained(save_path)

print(f"✅ 모델 저장 완료: {save_path}")

# 14. 테스트 예측
def predict_emotion(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(predictions, dim=-1).item()
    
    label_to_emotion = {v: k for k, v in emotion_to_label.items()}
    return label_to_emotion[predicted_class], predictions[0][predicted_class].item()

# 15. 테스트
test_texts = [
    "오늘 너무 행복해!",
    "정말 화가 나네",
    "슬픈 일이 생겼어",
    "그냥 평범한 하루"
]

print("\n🧪 모델 테스트 결과:")
for text in test_texts:
    emotion, confidence = predict_emotion(text)
    print(f"텍스트: '{text}' → 감정: {emotion} (신뢰도: {confidence:.3f})")

# 16. 모델 파일을 ZIP으로 압축 (다운로드 편의성)
!cd "/content/drive/MyDrive" && zip -r kobert_emotion_final.zip kobert_emotion_final/

print(f"""
🎉 학습 완료!

📁 저장된 파일들:
- 모델: /content/drive/MyDrive/kobert_emotion_final/
- ZIP: /content/drive/MyDrive/kobert_emotion_final.zip

📱 다음 단계:
1. Google Drive에서 ZIP 파일 다운로드
2. 로컬 프로젝트의 models/ 폴더에 압축 해제
3. FastAPI 서비스에서 모델 로드
4. 웹에서 실시간 감정 분석 서비스 제공

🔗 연결 방법은 COLAB_INTEGRATION_GUIDE.md 참조
""")