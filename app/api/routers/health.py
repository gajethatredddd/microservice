from fastapi import APIRouter
from app.core.exceptions import CustomException

router = APIRouter()

@router.get("/health", include_in_schema=True)
async def health_check():
    return {"status": "ok"}

@router.get("/raise_custom_error")
async def raise_custom_error():
    raise CustomException("кастомная ошибка", status_code=418)