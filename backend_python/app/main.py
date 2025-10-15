from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger
import sys
import os

from .database import SessionLocal, engine
from .models import Base
from .routers import auth, users, entries, emotions
from .config import settings
from .middleware import LoggingMiddleware
from .exceptions import (
    http_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler
)

# Create tables
Base.metadata.create_all(bind=engine)

# Configure logger
logger.remove()
logger.add(sys.stderr, level="INFO")

# logs 디렉토리가 없으면 생성
os.makedirs("logs", exist_ok=True)
logger.add("logs/app.log", rotation="500 MB", level="DEBUG", retention="30 days")

app = FastAPI(
    title="Emotion Diary API",
    description="A REST API for emotion diary application with emotion analysis",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Custom middleware
app.add_middleware(LoggingMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "*"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(entries.router, prefix="/api/entries", tags=["entries"])
app.include_router(emotions.router, prefix="/api/emotions", tags=["emotions"])

# Database dependency는 database.py에서 import
from .database import get_db

@app.get("/")
async def root():
    return {"message": "Emotion Diary API is running!"}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.DEBUG
    }

@app.get("/api/model/status")
async def model_status():
    """모델 상태 확인"""
    from .services.kobert_emotion_service import check_model_status
    return check_model_status()

# Exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

logger.info("Emotion Diary API initialized successfully")