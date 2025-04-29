import smtplib
from email.message import EmailMessage
from backend.config import EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD

import logging

logger = logging.getLogger(__name__)

def send_email(to_email: str, subject: str, body: str):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_USERNAME
        msg["To"] = to_email
        msg.set_content(body)

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        logger.info(f"Email sent successfully to {to_email}")

    except smtplib.SMTPConnectError:
        logger.error("Failed to connect to the SMTP server.")
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP authentication failed.")
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred: {e}")