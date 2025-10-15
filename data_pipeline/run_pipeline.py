#!/usr/bin/env python3
"""
데이터 파이프라인 통합 실행 스크립트
"""

import argparse
import sys
from pathlib import Path
import subprocess
from loguru import logger

def run_crawler(config_file: str = None):
    """데이터 크롤링 실행"""
    logger.info("🕷️ 데이터 크롤링 시작...")
    
    if config_file:
        cmd = ["python", "src/crawler.py", "--config", config_file]
    else:
        cmd = ["python", "src/crawler.py"]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        logger.info("✅ 크롤링 완료")
        return True
    else:
        logger.error(f"❌ 크롤링 실패: {result.stderr}")
        return False

def run_labeling_tool():
    """라벨링 도구 실행"""
    logger.info("🏷️ 라벨링 도구 시작...")
    
    cmd = ["streamlit", "run", "src/labeling_tool.py", "--server.port", "8501"]
    
    try:
        subprocess.run(cmd)
        return True
    except KeyboardInterrupt:
        logger.info("라벨링 도구 종료")
        return True
    except Exception as e:
        logger.error(f"❌ 라벨링 도구 실행 실패: {e}")
        return False

def run_training():
    """모델 학습 실행"""
    logger.info("🤖 모델 학습 시작...")
    
    cmd = ["python", "src/model_training.py"]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        logger.info("✅ 모델 학습 완료")
        return True
    else:
        logger.error(f"❌ 모델 학습 실패: {result.stderr}")
        return False

def setup_environment():
    """환경 설정"""
    logger.info("🔧 환경 설정 중...")
    
    # 필요한 디렉토리 생성
    dirs = ["data/raw", "data/processed", "data/models", "logs"]
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    # 의존성 설치
    cmd = ["pip", "install", "-r", "requirements.txt"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        logger.info("✅ 환경 설정 완료")
        return True
    else:
        logger.error(f"❌ 환경 설정 실패: {result.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description="감정 분석 데이터 파이프라인")
    parser.add_argument("command", choices=["setup", "crawl", "label", "train", "full"], 
                       help="실행할 명령")
    parser.add_argument("--config", help="크롤링 설정 파일")
    
    args = parser.parse_args()
    
    if args.command == "setup":
        setup_environment()
    
    elif args.command == "crawl":
        run_crawler(args.config)
    
    elif args.command == "label":
        run_labeling_tool()
    
    elif args.command == "train":
        run_training()
    
    elif args.command == "full":
        # 전체 파이프라인 실행
        logger.info("🚀 전체 데이터 파이프라인 시작...")
        
        if not setup_environment():
            sys.exit(1)
        
        if not run_crawler(args.config):
            sys.exit(1)
        
        logger.info("📋 라벨링을 위해 Streamlit 앱을 실행합니다.")
        logger.info("브라우저에서 http://localhost:8501로 접속하여 라벨링을 완료한 후 Ctrl+C로 종료하세요.")
        
        if not run_labeling_tool():
            sys.exit(1)
        
        if not run_training():
            sys.exit(1)
        
        logger.info("🎉 전체 파이프라인 완료!")

if __name__ == "__main__":
    main()