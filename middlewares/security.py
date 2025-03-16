from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import logging

logger = logging.getLogger("uvicorn")

class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Incoming request: {request.method} {request.url}")
        logger.debug(f"Request headers: {request.headers}")
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Error occurred while processing the request: {str(e)}")
            raise e

        return response