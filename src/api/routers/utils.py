import smtplib
from datetime import date
from email.mime.text import MIMEText

from fastapi import HTTPException

from src.config import settings


def send_email_service(emails: list, message: str = "", subject: str = ""):
    # если не надо скрывать получателей и отправляешь сразу рассылкой, это лучше, т.к. в лимите это одно письмо
    msg = MIMEText(message, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = "anikeev.maks@gmail.com"
    msg["To"] = ", ".join(emails)
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(msg["From"], settings.GOOGLE_EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"Письмо отправлено на адреса  {', '.join(emails)}")
    except Exception as e:
        print(f"Ошибка {e}")

    # это вариант рассылки отдельного письма на каждую почту
    for email in emails:
        msg = MIMEText(message, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = "anikeev.maks@gmail.com"
        msg["To"] = email
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(msg["From"], settings.GOOGLE_EMAIL_PASSWORD)
                server.send_message(msg)
                print(f"Письмо отправлено на адрес  {email}")
        except Exception as e:
            print(f"Ошибка {e}")


def check_date_to_after_date_from(date_from: date, date_to: date):
    if date_from >= date_to:
        raise HTTPException(
            status_code=400, detail="Дата выезда должна быть позже даты заезда"
        )
