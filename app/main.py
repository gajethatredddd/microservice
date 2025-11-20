from fastapi import FastAPI
from app.api.routers import messages
from app.core.exceptions import exception_handler, CustomException

def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI Celery Email App")

    @app.on_event("startup")
    async def startup():
        app.state.celery_app = "initialized"

    app.include_router(messages.router, prefix="/api")
    app.add_exception_handler(CustomException, exception_handler)

    return app

app = create_app()
