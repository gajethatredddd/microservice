from app.tasks.celery_tasks import send_email_task

# Почта, на которую хочешь отправить тест
recipient_email = "gajethatredddd@vk.com"

# ID картинки, которую хочешь протестировать
image_id = "1"

# Отправляем задачу в Celery
result = send_email_task.delay(recipient_email, image_id)

print(f"Задача отправлена, ID: {result.id}")
