from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status

class CustomException(Exception):
    def __init__(self, detail: str):
        self.detail = detail

async def exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.detail}
    )
