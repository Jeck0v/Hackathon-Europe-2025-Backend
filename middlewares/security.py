from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import logging

logger = logging.getLogger("uvicorn")

class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Incoming request: {request.method} {request.url}")
        response = await call_next(request)
        return response