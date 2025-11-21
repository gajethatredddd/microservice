from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from app.api.routers import messages, health
from app.core.exceptions import exception_handler, CustomException


# Асинхронный контекстный менеджер для lifespan
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Инициализация celery_app в состоянии приложения
    app.state.celery_app = "initialized"

    try:
        yield
    finally:
        # Очистка ресурса при завершении работы
        if hasattr(app.state, "celery_app"):
            app.state.celery_app = None


# Функция для создания FastAPI приложения
def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI Celery Email App", lifespan=lifespan)

    # Регистрация роутеров
    app.include_router(messages.router, prefix="/api")
    app.include_router(health.router, prefix="/api")

    # Добавление обработчика исключений
    app.add_exception_handler(CustomException, exception_handler)

    return app


# Создание экземпляра приложения
app = create_app()
