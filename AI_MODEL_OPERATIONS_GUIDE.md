# 🚀 AI 모델 운영 전략 가이드

## 🏢 기업 환경에서의 AI 모델 운영

### 📊 학습 단계 (Training Phase)
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   클라우드 GPU    │    │  온프레미스 GPU   │    │   ML 플랫폼      │
│   (AWS/GCP/Azure)│    │   (DGX 서버)     │    │ (Kubeflow/MLflow)│
│   - p3.xlarge    │    │   - A100 x8     │    │  - 파이프라인     │
│   - V100/A100    │    │   - 24/7 운영    │    │  - 실험 관리     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 💾 모델 저장 및 버전 관리
```python
# MLflow를 통한 모델 관리
import mlflow
import mlflow.pytorch

# 모델 학습 후 등록
with mlflow.start_run():
    mlflow.pytorch.log_model(model, "kobert_emotion_v1.0")
    mlflow.log_params({"epochs": 10, "batch_size": 32})
    mlflow.log_metrics({"accuracy": 0.95, "f1_score": 0.93})

# 프로덕션 등록
mlflow.register_model("runs:/run_id/kobert_emotion", "KoBERT_Emotion_Prod")
```

### 🌐 프로덕션 서빙 아키텍처
```
Internet → Load Balancer → API Gateway → FastAPI Pods → Model Registry
                                      ↓
                               Redis Cache (모델 로드)
                                      ↓
                            Monitoring (Prometheus/Grafana)
```

## 👤 개인 프로젝트 운영 전략

### 💰 비용 효율적인 방법들

#### 1️⃣ **무료/저비용 학습**
- **Google Colab Pro** ($10/월): 더 긴 세션, 우선 GPU 접근
- **Kaggle Notebooks**: 주 30시간 무료 GPU
- **AWS Spot Instances**: 90% 할인된 GPU 인스턴스
- **Vast.ai**: 개인 GPU 임대 플랫폼

#### 2️⃣ **모델 저장 전략**
```python
# Hugging Face Hub (무료)
model.push_to_hub("your-username/kobert-emotion-korean")

# GitHub LFS (대용량 파일)
git lfs track "*.bin"
git add model/pytorch_model.bin
git commit -m "Add trained model"

# Google Drive API
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
# 자동 업로드/다운로드
```

#### 3️⃣ **서버리스 배포**
```python
# Hugging Face Spaces (무료 호스팅)
# gradio_app.py
import gradio as gr
from transformers import pipeline

classifier = pipeline("text-classification", 
                     model="your-username/kobert-emotion-korean")

def predict(text):
    result = classifier(text)
    return result[0]['label'], result[0]['score']

demo = gr.Interface(fn=predict, 
                   inputs="text", 
                   outputs=["text", "number"])
demo.launch()
```

### 🔄 **모델 지속성 확보 방법**

#### A. **클라우드 기반 (권장)**
```yaml
# docker-compose.yml
version: '3.8'
services:
  emotion-api:
    image: your-dockerhub/emotion-diary:latest
    environment:
      - MODEL_PATH=https://huggingface.co/your-username/kobert-emotion
    volumes:
      - model_cache:/app/models
    restart: unless-stopped

volumes:
  model_cache:
```

#### B. **GitHub Actions CI/CD**
```yaml
# .github/workflows/deploy.yml
name: Auto Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to VPS
        run: |
          ssh user@your-vps.com "cd /app && git pull && docker-compose up -d"
```

#### C. **모델 캐싱 전략**
```python
# 스마트 모델 로딩
import os
from pathlib import Path
from transformers import AutoModel, AutoTokenizer

class ModelManager:
    def __init__(self, model_name="your-username/kobert-emotion"):
        self.model_name = model_name
        self.cache_dir = Path("./model_cache")
        self.model = None
        self.tokenizer = None
    
    def load_model(self):
        # 로컬 캐시 확인
        if (self.cache_dir / "pytorch_model.bin").exists():
            print("📦 로컬 캐시에서 모델 로드")
            self.model = AutoModel.from_pretrained(self.cache_dir)
            self.tokenizer = AutoTokenizer.from_pretrained(self.cache_dir)
        else:
            print("🌐 Hugging Face Hub에서 모델 다운로드")
            self.model = AutoModel.from_pretrained(self.model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # 로컬에 캐시 저장
            self.model.save_pretrained(self.cache_dir)
            self.tokenizer.save_pretrained(self.cache_dir)
```

## 🎯 **개인 프로젝트 추천 워크플로우**

### 단계별 구현
```
1. 개발 단계
   └── Google Colab (무료) → 모델 학습
   └── Hugging Face Hub → 모델 저장
   └── GitHub → 코드 저장

2. 테스트 단계  
   └── 로컬 환경 → API 개발
   └── Docker → 컨테이너화
   └── 클라우드 VPS → 배포 테스트

3. 운영 단계
   └── 저비용 VPS (월 $5-20)
   └── Docker + nginx
   └── GitHub Actions → 자동 배포
```

### 💡 **실제 비용 예시**
```
🆓 무료 옵션:
- Colab (기본): 무료
- Hugging Face Spaces: 무료 호스팅
- GitHub Actions: 월 2,000분 무료
- Heroku (제한적): 무료 티어

💰 저비용 옵션:
- Colab Pro: $10/월
- DigitalOcean Droplet: $5-20/월  
- AWS EC2 t3.micro: $8-15/월
- Railway/Render: $5-10/월
```

## 🚨 **세션 지속성 해결책**

### Colab 12시간 제한 우회
1. **Colab Pro**: 24시간 세션
2. **자동 재연결 스크립트**:
```javascript
// 브라우저 콘솔에서 실행
setInterval(() => {
    document.querySelector("colab-toolbar-button").click()
}, 60000)
```

3. **체크포인트 저장**:
```python
# 주기적 모델 저장
for epoch in range(epochs):
    # 학습...
    if epoch % 5 == 0:  # 5 에포크마다 저장
        model.save_pretrained(f"/content/drive/MyDrive/checkpoint_epoch_{epoch}")
```

결론적으로, **개인 프로젝트라면 Colab에서 학습 → Hugging Face Hub 저장 → 저비용 VPS 배포**가 가장 실용적입니다! 🎉