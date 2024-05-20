from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from src.utils.settings import get_settings
from pydantic import EmailStr

settings = get_settings()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=settings.mail_tls,
    MAIL_SSL_TLS=settings.mail_ssl,
    USE_CREDENTIALS=settings.use_credentials,
)


async def send_magic_link(email: EmailStr, token: str):
    message = MessageSchema(
        subject="Magic Link Login",
        recipients=[email],
        body=f"Click the link to login: {settings.backend_url}/auth/magic-link?token={token}",
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
