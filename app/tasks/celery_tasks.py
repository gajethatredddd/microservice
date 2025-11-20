from celery import Celery
from app.core.config import settings
from app.services.message_service import MessageService

# Инициализация Celery с RabbitMQ
celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BACKEND_URL,
)

celery_app.autodiscover_tasks()


@celery_app.task
def send_email_task(to_email: str, image_id: str):
    """
    Celery-задача: получить текст с внешнего API и отправить письмо.
    """
    service = MessageService()

    # 1. Получаем текст из API (OCR / анализ)
    extracted_text = service.fetch_text_from_external_api(image_id)

    # 2. Формируем текст письма
    subject = f"Analysis result for image {image_id}"
    body = f"Картинка {image_id} успешно обработана.\n\nИзвлечённый текст:\n\n{extracted_text}"

    # 3. Отправка email — уже внутри MessageService
    service.send_email(
        to_email=to_email,
        subject=subject,
        body=body
    )

    return {
        "status": "sent",
        "email": to_email,
        "image_id": image_id
    }
