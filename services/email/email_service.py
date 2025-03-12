import smtplib
import ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.office365.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))


def send_email(to_email: str, subject: str, content: str, html: bool = False):
    """
    Sends an email with the given subject and content.
    Supports both plain text and HTML emails.

    :param to_email: Recipient email address
    :param subject: Email subject
    :param content: Email body (plain text or HTML)
    :param html: Set to True to send HTML email
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email

    if html:
        msg.add_alternative(content, subtype="html")
    else:
        msg.set_content(content)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"✅ Email sent to {to_email}")
            return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False
