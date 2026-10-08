import smtplib
import os

from email.message import EmailMessage
from dotenv import load_dotenv


load_dotenv()


def send_otp_email(receiver_email, otp):

    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("APP_PASSWORD")

    message = EmailMessage()

    message["Subject"] = "Your OTP - Three Level Authentication"
    message["From"] = sender_email
    message["To"] = receiver_email

    message.set_content(
        f"""
Hello,

Your OTP for Three Level Authentication is:

{otp}

This OTP is valid for 5 minutes.

Do not share this OTP with anyone.

Thank you.
"""
    )

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(sender_email, app_password)

        server.send_message(message)

        server.quit()

        print("OTP sent successfully to your email!")

        return True

    except Exception as e:

        print("Failed to send OTP.")
        print(e)

        return False
