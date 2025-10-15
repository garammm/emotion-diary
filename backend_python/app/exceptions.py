from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger
from typing import Union
import traceback

class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code

async def http_exception_handler(request: Request, exc: HTTPException):
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    logger.error(
        f"[{request_id}] HTTP Exception: {exc.status_code} - {exc.detail} - "
        f"URL: {request.url}"
    )
    
    error_response = {
        "error": {
            "code": exc.status_code,
            "message": exc.detail,
            "request_id": request_id
        }
    }
    
    if hasattr(exc, 'error_code') and exc.error_code:
        error_response["error"]["error_code"] = exc.error_code
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response,
        headers={"X-Request-ID": request_id}
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    logger.error(
        f"[{request_id}] Validation Error: {exc.errors()} - "
        f"URL: {request.url}"
    )
    
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": 422,
                "message": "Validation error",
                "details": exc.errors(),
                "request_id": request_id
            }
        },
        headers={"X-Request-ID": request_id}
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    logger.error(
        f"[{request_id}] Database Error: {str(exc)} - "
        f"URL: {request.url}"
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": 500,
                "message": "Database error occurred",
                "request_id": request_id
            }
        },
        headers={"X-Request-ID": request_id}
    )

async def general_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    logger.error(
        f"[{request_id}] Unhandled Exception: {str(exc)} - "
        f"URL: {request.url} - "
        f"Traceback: {traceback.format_exc()}"
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": 500,
                "message": "Internal server error",
                "request_id": request_id
            }
        },
        headers={"X-Request-ID": request_id}
    )

# 커스텀 예외 클래스들
class UserNotFoundError(CustomHTTPException):
    def __init__(self, user_id: Union[int, str]):
        super().__init__(
            status_code=404,
            detail=f"User with id {user_id} not found",
            error_code="USER_NOT_FOUND"
        )

class EntryNotFoundError(CustomHTTPException):
    def __init__(self, entry_id: int):
        super().__init__(
            status_code=404,
            detail=f"Entry with id {entry_id} not found",
            error_code="ENTRY_NOT_FOUND"
        )

class UnauthorizedError(CustomHTTPException):
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(
            status_code=401,
            detail=message,
            error_code="UNAUTHORIZED"
        )

class ForbiddenError(CustomHTTPException):
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(
            status_code=403,
            detail=message,
            error_code="FORBIDDEN"
        )

class ValidationError(CustomHTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=400,
            detail=message,
            error_code="VALIDATION_ERROR"
        )