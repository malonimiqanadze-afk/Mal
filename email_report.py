import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from getpass import getpass

from config import load_dotenv

load_dotenv()

# Read from .env / real environment variables; never hardcoded in source.
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "quotes@yourcompany.com")


def send_email_report(report_text, recipient_email):
  # Password is never hardcoded in source; read from .env/env var, falling
  # back to an interactive (hidden) prompt.
  sender_password = os.environ.get("EMAIL_APP_PASSWORD") or getpass(
      f"App Password for {SENDER_EMAIL}: "
  )

  if not sender_password or not recipient_email:
    print("Missing sender password or recipient email. Skipping email.")
    return

  try:
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email
    msg["Subject"] = "Removals Volume & Packing Estimate Report"
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid()
    msg.attach(MIMEText(report_text, "plain"))

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SENDER_EMAIL, sender_password)
    server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
    server.quit()
    print(f"Successfully emailed report to {recipient_email}!")
  except Exception as e:
    print(f"Failed to send email. Error: {e}")

