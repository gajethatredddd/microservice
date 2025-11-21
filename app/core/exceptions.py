from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status

# Обновленный класс CustomException с поддержкой status_code
class CustomException(Exception):
    def __init__(self, detail: str, status_code: int = 400):  # добавлен параметр status_code
        self.detail = detail
        self.status_code = status_code

# Обработчик исключений для CustomException
async def exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,  # используем status_code из CustomException
        content={"detail": exc.detail}
    )

