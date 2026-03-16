import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your@email.com"
SMTP_PASSWORD = "yourpassword"


def send_email(to_email: str, subject: str, message: str):

    try:

        msg = MIMEMultipart()

        msg["From"] = SMTP_USER
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()

        server.login(SMTP_USER, SMTP_PASSWORD)

        server.sendmail(SMTP_USER, to_email, msg.as_string())

        server.quit()

        print(f"Email sent to {to_email}")

    except Exception as e:

        print("Email error:", e)
