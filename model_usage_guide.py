"""
학습된 모델 파일 구조 및 사용법 설명
"""

# 학습 완료 후 생성되는 파일 구조:
"""
models/kobert_emotion/
├── pytorch_model.bin          # 학습된 모델 가중치 (가장 중요!)
├── config.json                # 모델 설정 (레이어 구조, 클래스 수 등)
├── tokenizer.json             # 토크나이저 설정
├── tokenizer_config.json      # 토크나이저 구성
├── special_tokens_map.json    # 특수 토큰 매핑
└── vocab.txt                  # 어휘 사전
"""

# 1. 학습 중 자동 저장 (model_training.py에서)
def train_model(self, train_dataset, val_dataset, output_dir: str = "models/kobert_emotion"):
    # ... 학습 코드 ...
    
    # 학습 완료된 모델을 디스크에 저장
    trainer.save_model()                    # 모델 가중치 저장
    self.tokenizer.save_pretrained(output_dir)  # 토크나이저 저장
    
    logger.info(f"모델 학습 완료. 저장 위치: {output_dir}")


# 2. 서비스에서 모델 로딩 (kobert_emotion_service.py에서)
def _load_model(self):
    try:
        logger.info(f"KoBERT 모델 로딩: {self.model_path}")
        
        # 디스크에서 토크나이저 로드
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        
        # 디스크에서 학습된 모델 로드
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
        
        # GPU/CPU로 모델 이동
        self.model.to(self.device)
        self.model.eval()  # 추론 모드로 설정
        
        logger.info(f"KoBERT 모델 로딩 완료 (Device: {self.device})")
        
    except Exception as e:
        logger.error(f"KoBERT 모델 로딩 실패: {e}")


# 3. 추론 시 모델 사용
def _predict_with_kobert(self, text: str):
    # 토크나이징
    inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    
    # GPU로 이동
    inputs = {key: value.to(self.device) for key, value in inputs.items()}
    
    # 추론 (그래디언트 계산 비활성화로 메모리 절약)
    with torch.no_grad():
        outputs = self.model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    return predictions