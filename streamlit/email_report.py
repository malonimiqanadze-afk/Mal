import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass


def send_email_report(report_text):
  answer = input("\nEmail this report? (y/N): ").strip().lower()
  if answer != "y":
    return

  sender_email = input("Company Email Address: ").strip()
  sender_password = getpass("App Password (16-digit): ")
  recipient_email = input("Recipient Email Address: ").strip()

  if not sender_email or not sender_password or not recipient_email:
    print("Please fill in all email fields. Skipping email.")
    return

  try:
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = "Removals Volume & Packing Estimate Report"
    msg.attach(MIMEText(report_text, "plain"))

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()
    print(f"Successfully emailed report to {recipient_email}!")
  except Exception as e:
    print(f"Failed to send email. Error: {e}")
