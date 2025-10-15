# Colab에서 모델 학습 후 웹서비스 연결 가이드

## 🚀 단계별 프로세스

### 1️⃣ Colab에서 모델 학습
```python
# Colab 노트북에서
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from google.colab import drive
import torch

# Google Drive 마운트
drive.mount('/content/drive')

# 모델 학습 코드...
trainer.train()

# 모델 저장 (Google Drive에)
model_save_path = "/content/drive/MyDrive/kobert_emotion_model"
trainer.save_model(model_save_path)
tokenizer.save_pretrained(model_save_path)

# 파일을 ZIP으로 압축
!cd "/content/drive/MyDrive" && zip -r kobert_emotion_model.zip kobert_emotion_model/
```

### 2️⃣ 학습된 모델을 로컬로 다운로드
```bash
# Google Drive에서 ZIP 파일 다운로드
# models/ 폴더에 압축 해제
```

### 3️⃣ FastAPI에서 학습된 모델 로드
```python
# kobert_emotion_service.py에서
class KoBERTEmotionAnalyzer:
    def __init__(self, model_path: str = "models/kobert_emotion_model"):
        self.model_path = model_path
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.eval()
    
    def predict(self, text: str):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        return predictions
```

### 4️⃣ 웹 API로 서비스
```python
# FastAPI 엔드포인트
@app.post("/api/emotions/analyze")
async def analyze_emotion(text: str):
    analyzer = get_kobert_analyzer()  # 싱글톤 패턴
    result = analyzer.predict(text)
    return {"emotion": result["emotion_type"], "confidence": result["confidence_score"]}
```

## 💾 **모델 상태 유지 방법**

### A. **파일 기반 저장**
```python
# 학습 후 저장
trainer.save_model("./models/kobert_emotion")
tokenizer.save_pretrained("./models/kobert_emotion")

# 서비스에서 로드
model = AutoModelForSequenceClassification.from_pretrained("./models/kobert_emotion")
```

### B. **클라우드 저장소**
```python
# Hugging Face Hub에 업로드
model.push_to_hub("your-username/kobert-emotion-korean")

# 서비스에서 다운로드
model = AutoModelForSequenceClassification.from_pretrained("your-username/kobert-emotion-korean")
```

### C. **Docker Image에 포함**
```dockerfile
# Dockerfile
COPY models/kobert_emotion /app/models/kobert_emotion
```

## 🔄 **추천 워크플로우**

### 개발 단계:
1. **Colab**: 모델 학습 (무료 GPU 활용)
2. **Google Drive**: 학습된 모델 저장
3. **로컬**: 모델 다운로드 후 API 통합
4. **Docker**: 모델 포함한 컨테이너 빌드
5. **K8s**: 프로덕션 배포

### 운영 단계:
- **모델 업데이트**: Colab에서 재학습 → 새 버전 배포
- **A/B 테스트**: 구버전/신버전 모델 동시 서비스
- **모니터링**: 모델 성능 추적