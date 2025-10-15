# 감정 다이어리 애플리케이션

Python FastAPI 백엔드, React 프론트엔드, Kubernetes 배포를 지원하는 현대적인 감정 다이어리 애플리케이션입니다.

## 🚀 주요 기능

- **완전한 데이터 파이프라인**: 크롤링 → 라벨링 → 검수 → KoBERT 파인튜닝
- **REST API**: FastAPI 기반 백엔드와 자동 OpenAPI 문서
- **AI 감정 분석**: KoBERT 기반 한국어 감정 분석 (7개 감정 분류)
- **사용자 인증**: JWT 기반 인증 및 권한 관리
- **데이터베이스**: PostgreSQL + SQLAlchemy ORM
- **프론트엔드**: React 기반 모던 UI
- **컨테이너화**: 모든 서비스 Docker 컨테이너화
- **오케스트레이션**: Kubernetes 배포 및 스케일링
- **CI/CD**: GitHub Actions 자동화 파이프라인
- **모니터링**: 헬스체크 및 구조화된 로깅

## 🏗️ 시스템 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React         │    │   FastAPI       │    │   PostgreSQL    │
│   프론트엔드      │◄──►│   백엔드         │◄──►│   데이터베이스    │
│   (Port 3000)   │    │   (Port 8000)   │    │   (Port 5432)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                       ┌─────────────────┐
                       │     Redis       │
                       │     캐시         │
                       │   (Port 6379)   │
                       └─────────────────┘
```

## � 데이터 파이프라인 

```
데이터 수집 → 반자동 라벨링 → 검수 → 전처리 → KoBERT 파인튜닝 → 서비스 통합
   (크롤링)     (Streamlit)    (수동)   (정제)    (Hugging Face)   (FastAPI)
```

## 📋 사전 요구사항

- Docker 및 Docker Compose
- Kubernetes 클러스터 (minikube, kind, 또는 클라우드)
- kubectl CLI 도구
- Node.js 18+ 및 Yarn
- Python 3.11+

## 🚀 빠른 시작

### 1. Docker Compose로 로컬 개발

```bash
# 저장소 클론
git clone https://github.com/garammm/emotion-diary.git
cd emotion-diary

# 모든 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 애플리케이션 접속
# 프론트엔드: http://localhost:3000
# 백엔드 API: http://localhost:8000
# API 문서: http://localhost:8000/api/docs
```

### 2. 데이터 파이프라인 실행

```bash
# 데이터 파이프라인 디렉토리로 이동
cd data_pipeline

# 환경 설정
python run_pipeline.py setup

# 전체 파이프라인 실행 (크롤링 → 라벨링 → 학습)
python run_pipeline.py full --config config.yaml

# 또는 단계별 실행
python run_pipeline.py crawl --config config.yaml  # 데이터 수집
python run_pipeline.py label                        # 라벨링 (http://localhost:8501)
python run_pipeline.py train                        # 모델 학습
```

### 3. Kubernetes 배포

```bash
# 이미지 빌드 및 푸시 (레지스트리 주소 수정 필요)
docker build -t your-registry/emotion-diary-backend:latest ./backend_python
docker build -t your-registry/emotion-diary-frontend:latest .

# Kubernetes 배포
cd k8s
chmod +x deploy.sh
./deploy.sh

# Windows의 경우
deploy.cmd

# Ingress 접속 (hosts 파일 수정)
echo "127.0.0.1 emotion-diary.local" >> /etc/hosts
# 브라우저에서 http://emotion-diary.local 접속
```

## 🛠️ 개발 환경 설정

### 백엔드 개발

```bash
cd backend_python

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일 수정

# 개발 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 테스트 실행
pytest tests/ -v

# API 문서: http://localhost:8000/api/docs
```

### 프론트엔드 개발

```bash
# 의존성 설치
yarn install

# 개발 서버 시작
yarn start

# 테스트 실행
yarn test

# 프로덕션 빌드
yarn build
```

## 📊 API 엔드포인트

### 인증
- `POST /api/auth/register` - 사용자 회원가입
- `POST /api/auth/token` - 사용자 로그인
- `GET /api/auth/me` - 현재 사용자 정보

### 사용자 관리
- `GET /api/users/` - 사용자 목록
- `GET /api/users/{id}` - 사용자 상세 정보
- `PUT /api/users/{id}` - 사용자 정보 수정
- `DELETE /api/users/{id}` - 사용자 삭제

### 일기 관리
- `POST /api/entries/` - 일기 작성
- `GET /api/entries/` - 내 일기 목록
- `GET /api/entries/{id}` - 일기 상세 조회
- `PUT /api/entries/{id}` - 일기 수정
- `DELETE /api/entries/{id}` - 일기 삭제
- `GET /api/entries/{id}/analyze` - 일기 감정 분석

### 감정 분석
- `GET /api/emotions/` - 감정 분석 결과 목록
- `POST /api/emotions/analyze` - 텍스트 감정 분석
- `GET /api/emotions/stats/summary` - 감정 통계
- `DELETE /api/emotions/{id}` - 감정 분석 결과 삭제

### 시스템
- `GET /api/health` - 서비스 상태 확인
- `GET /api/model/status` - AI 모델 상태 확인

## 🤖 감정 분석 모델

### 지원하는 감정 (7개 클래스)
- **중립** (0): 평범하고 특별한 감정이 없는 상태
- **기쁨** (1): 행복, 즐거움, 만족감
- **슬픔** (2): 우울, 속상함, 실망감  
- **분노** (3): 화남, 짜증, 불만
- **두려움** (4): 무서움, 걱정, 불안감
- **놀라움** (5): 깜짝 놀람, 의외, 충격
- **혐오** (6): 싫어함, 거부감, 역겨움

### 모델 정보
- **기반 모델**: KLUE-BERT (한국어 특화)
- **학습 방법**: 파인튜닝 (Fine-tuning)
- **데이터**: 크롤링 + 수동 라벨링
- **성능**: 실시간 분석 지원

## 🔧 환경 설정

### 백엔드 환경변수 (.env)
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/emotion_diary
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
```

### 프론트엔드 환경변수 (.env.local)
```bash
REACT_APP_API_BASE_URL=http://localhost:8000/api
```

## 🚀 배포

### GitHub Actions CI/CD

완전한 CI/CD 파이프라인이 포함되어 있습니다:

1. **테스트**: 백엔드 및 프론트엔드 테스트 실행
2. **보안**: Trivy를 이용한 취약점 스캔
3. **빌드**: Docker 이미지 생성
4. **배포**: Kubernetes 클러스터에 자동 배포

필요한 GitHub Secrets:
- `DOCKER_USERNAME`: Docker Hub 사용자명
- `DOCKER_PASSWORD`: Docker Hub 비밀번호/토큰
- `KUBE_CONFIG`: Base64 인코딩된 kubeconfig 파일
- `SLACK_WEBHOOK_URL`: (선택사항) Slack 알림

## 📊 모니터링 및 로깅

### 애플리케이션 로그
- 백엔드 로그: `logs/app.log`에 저장
- 요청 ID 기반 구조화된 로깅
- 로그 로테이션 (500MB 파일, 30일 보관)

### 헬스체크
- 백엔드: `GET /api/health`
- 프론트엔드: `GET /health`
- 데이터베이스: PostgreSQL 내장 헬스체크

## 🔒 보안

- JWT 기반 인증
- bcrypt 비밀번호 암호화
- SQLAlchemy ORM으로 SQL 인젝션 방지
- CORS 설정
- Docker 보안 모범사례
- Kubernetes 보안 컨텍스트

## 📁 프로젝트 구조

```
emotion-diary/
├── backend_python/           # FastAPI 백엔드
│   ├── app/
│   │   ├── routers/         # API 라우터
│   │   ├── models/          # 데이터베이스 모델
│   │   ├── services/        # 비즈니스 로직
│   │   └── main.py          # 애플리케이션 진입점
│   ├── tests/               # 테스트 코드
│   └── Dockerfile
├── data_pipeline/           # 데이터 파이프라인
│   ├── src/
│   │   ├── crawler.py       # 데이터 크롤링
│   │   ├── labeling_tool.py # 라벨링 도구
│   │   └── model_training.py# 모델 학습
│   └── config.yaml          # 크롤링 설정
├── src/                     # React 프론트엔드
├── k8s/                     # Kubernetes 매니페스트
├── .github/workflows/       # CI/CD 파이프라인
├── docker-compose.yml       # 로컬 개발환경
└── README.md
```

## 🤝 기여하기

1. 저장소를 포크합니다
2. 기능 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다

## � 업데이트 예정

- [ ] 실시간 감정 변화 추적
- [ ] 감정 통계 시각화 대시보드  
- [ ] 다중 언어 지원
- [ ] 음성 일기 감정 분석
- [ ] 모바일 앱 개발

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
