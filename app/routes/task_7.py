import logging
from contextvars import ContextVar
import logging.config
from pathlib import Path
from time import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logging.config.fileConfig(r"./app/files/log.config")
output_log = logging.getLogger("output")
client_host: ContextVar[str | None] = ContextVar("client_host", default=None)
parameters = {"duration": 0, "method": "", "url": "", "status": ""}
output_log = logging.LoggerAdapter(output_log, parameters)

GLOBAL_TIME = time()


"""
Задание_7. Логирование в FastAPI с использованием middleware.

Написать конфигурационный файл для логгера "output"
Формат выводимых логов:
[CURRENT_DATETIME] {file: line} LOG_LEVEL - | EXECUTION_TIME_SEC | HTTP_METHOD | URL | STATUS_CODE |
[2023-12-15 00:00:00] {example:62} INFO | 12 | GET | http://localhost/example | 200 |


Дописать класс CustomMiddleware.
Добавить middleware в приложение (app).
"""
class CustomMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        """Load request ID from headers if present. Generate one otherwise."""

        try:
            global output_log
            global GLOBAL_TIME
            
            client_host.set(request.client.host)
            duration = time() - GLOBAL_TIME 
            
            response = await call_next(request)
            
            GLOBAL_TIME = time()
            
            output_log.extra = {"duration": round(duration),
                                "method": request.method,
                                "url": request.url,
                                "status": response.status_code}
            output_log.info(f"Accepted request {request.method} {request.url}")

            return response
        except Exception as e:
            response = Response("Internal Server Error", status_code=500)
            return response

