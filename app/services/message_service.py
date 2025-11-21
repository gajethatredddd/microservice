import requests
from requests.exceptions import RequestException
import smtplib
from email.message import EmailMessage
from app.core.config import settings

class MessageService:
    def __init__(self):
        # SMTP настройки
        self.smtp_host = settings.MAIL_SERVER
        self.smtp_port = settings.MAIL_PORT
        self.smtp_user = settings.MAIL_USERNAME
        self.smtp_password = settings.MAIL_PASSWORD
        self.email_from = settings.MAIL_FROM
        self.use_ssl = settings.MAIL_SSL
        self.use_tls = settings.MAIL_TLS

        # Базовый URL внешнего API
        self.external_api_base = "http://web:8000/api/v1/lol"

    def fetch_text_from_external_api(self, image_id: str) -> str:
        """
        Берёт текст с картинки через внешний API.
        :param image_id: ID картинки
        :return: извлечённый текст
        """
        url = f"{self.external_api_base}/{image_id}/"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if "extracted_text" not in data:
                raise ValueError(f"'extracted_text' нету по этому айди {image_id}")
            return data["extracted_text"]
        except RequestException as e:
            raise RuntimeError(f"Error fetching data from external API: {e}")

    def send_email(self, to_email: str, subject: str, body: str):
        """
        Отправляет письмо на указанную почту.
        :param to_email: адрес получателя
        :param subject: тема письма
        :param body: тело письма
        """
        msg = EmailMessage()
        msg['From'] = self.email_from
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.set_content(body)

        # Отправка письма через SMTP
        if self.use_ssl:
            # SSL соединение
            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
        else:
            # TLS соединение
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

        print(f"Email sent to {to_email} with subject '{subject}'")
