# 감정 분석 데이터 파이프라인

완전한 데이터 파이프라인으로 감정 분석 모델을 학습시키는 도구입니다.

## 🏗️ 파이프라인 구조

```
데이터 수집 (크롤링) → 반자동 라벨링 → 검수 → 전처리 → KoBERT 파인튜닝
```

## 📦 설치

```bash
cd data_pipeline
pip install -r requirements.txt
```

## 🚀 사용법

### 1. 환경 설정
```bash
python run_pipeline.py setup
```

### 2. 데이터 수집 (크롤링)
```bash
python run_pipeline.py crawl --config config.yaml
```

### 3. 데이터 라벨링
```bash
python run_pipeline.py label
```
웹 브라우저에서 http://localhost:8501 접속하여 라벨링 진행

### 4. 모델 학습
```bash
python run_pipeline.py train
```

### 5. 전체 파이프라인 실행
```bash
python run_pipeline.py full --config config.yaml
```

## 📊 데이터 소스

- **네이버 카페**: 일상 글, 감정 관련 게시물
- **디시인사이드**: 다양한 갤러리의 글과 댓글  
- **블로그**: 감정 키워드로 검색된 포스트
- **뉴스 댓글**: (향후 추가 예정)

## 🏷️ 감정 라벨

- 0: 중립
- 1: 기쁨  
- 2: 슬픔
- 3: 분노
- 4: 두려움
- 5: 놀라움
- 6: 혐오

## 🤖 모델

- **기본 모델**: klue/bert-base (KoBERT)
- **파인튜닝**: 감정 분류 태스크에 특화
- **출력**: 7개 감정 클래스 확률

## 📁 파일 구조

```
data_pipeline/
├── src/
│   ├── crawler.py          # 데이터 크롤링
│   ├── labeling_tool.py    # 라벨링 도구
│   └── model_training.py   # 모델 학습
├── data/
│   ├── raw/               # 원본 크롤링 데이터
│   ├── processed/         # 전처리된 데이터
│   └── models/           # 학습된 모델
├── config.yaml           # 크롤링 설정
├── requirements.txt      # 패키지 의존성
└── run_pipeline.py      # 파이프라인 실행기
```

## ⚠️ 주의사항

1. **저작권**: 크롤링 시 해당 사이트의 robots.txt와 이용약관을 준수하세요.
2. **요청 제한**: 과도한 요청으로 IP 차단을 방지하기 위해 적절한 지연시간을 설정하세요.
3. **데이터 품질**: 라벨링 작업이 모델 성능에 직접적인 영향을 미치므로 신중하게 진행하세요.

## 🔧 커스터마이징

`config.yaml` 파일을 수정하여 크롤링 대상과 설정을 변경할 수 있습니다.