from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
import time
import uuid

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 요청 ID 생성
        request_id = str(uuid.uuid4())[:8]
        
        # 요청 로깅
        start_time = time.time()
        client_ip = request.client.host
        method = request.method
        url = str(request.url)
        
        logger.info(f"[{request_id}] {method} {url} - Client: {client_ip}")
        
        # 요청 처리
        try:
            response = await call_next(request)
            
            # 응답 로깅
            process_time = time.time() - start_time
            status_code = response.status_code
            
            logger.info(
                f"[{request_id}] {method} {url} - "
                f"Status: {status_code} - "
                f"Time: {process_time:.4f}s"
            )
            
            # 응답 헤더에 요청 ID 추가
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            # 예외 로깅
            process_time = time.time() - start_time
            logger.error(
                f"[{request_id}] {method} {url} - "
                f"Error: {str(e)} - "
                f"Time: {process_time:.4f}s"
            )
            
            # 에러 응답 반환
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