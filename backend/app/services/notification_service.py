# notification for long audits

import logging
from typing import Optional
import os
import aiosmtplib
from email.message import EmailMessage

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url
        # Load Mailtrap config from environment
        self.smtp_host = os.getenv("MAILTRAP_HOST")
        self.smtp_port = int(os.getenv("MAILTRAP_PORT", "587"))
        self.smtp_username = os.getenv("MAILTRAP_USERNAME")
        self.smtp_password = os.getenv("MAILTRAP_PASSWORD")
        self.from_email = os.getenv("MAILTRAP_FROM")

    async def notify_long_audit(self, audit_id: int, user_email: Optional[str] = None):
        """
        Notify the user that an audit is taking longer than expected.
        """
        message = f"Audit {audit_id} is taking longer than expected."
        logger.info(message)
        if user_email:
            await self.send_email(user_email, "Audit Delayed", message)
        if self.webhook_url:
            await self.send_webhook(message)

    async def notify_audit_complete(self, audit_id: int, user_email: Optional[str] = None):
        """
        Notify the user that an audit has completed.
        """
        message = f"Audit {audit_id} has completed."
        logger.info(message)
        if user_email:
            await self.send_email(user_email, "Audit Complete", message)
        if self.webhook_url:
            await self.send_webhook(message)

    async def send_email(self, to_email: str, subject: str, body: str):
        """
        Send an email using Mailtrap SMTP.
        """
        logger.info(f"Sending email to {to_email}: {subject} - {body}")
        msg = EmailMessage()
        msg["From"] = self.from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)
        await aiosmtplib.send(
            msg,
            hostname=self.smtp_host,
            port=self.smtp_port,
            username=self.smtp_username,
            password=self.smtp_password,
            start_tls=True,
        )

    async def send_webhook(self, message: str):
        """
        Integrate with your webhook provider here.
        This is a stub; replace with actual webhook logic.
        """
        logger.info(f"Sending webhook: {message}")
        # Implement webhook logic here if needed
        pass