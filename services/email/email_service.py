import smtplib
import ssl
from email.message import EmailMessage
import os
from root.root_elements import Settings

settings = Settings()

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
    msg["From"] = settings.EMAIL_SENDER
    msg["To"] = to_email

    if html:
        msg.add_alternative(content, subtype="html")
    else:
        msg.set_content(content)

    try:
        # ✅ Use standard SMTP, not SSL
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.ehlo()  # ✅ Identify with the SMTP server
        server.starttls()  # ✅ Upgrade connection to secure TLS
        server.ehlo()
        server.login(settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)  # ✅ Login securely
        server.send_message(msg)
        server.quit()  # ✅ Close the connection

        print(f"✅ Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False
