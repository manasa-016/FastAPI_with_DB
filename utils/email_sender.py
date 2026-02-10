import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()
app_password=os.environ["APP_PASSWORD"]
sender_email=os.environ["SENDER_EMAIL"]


# Email details
def send_email(receiver_email:str,subject:str,content:str) -> str:
    """Send an email to the specified receiver."""
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.set_content(content)

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

    return f"Email sent to {receiver_email} successfully ✅"



