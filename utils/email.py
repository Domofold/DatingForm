import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    def __init__(self):
        pass

    @staticmethod
    def sendEmailNotification(name, age, gender, dwelling_place, hobbies, diet, email):
        subject = f"New form from {name}!"
        body = (f"Name: {name}\n"
                f"Age: {age}\n"
                f"Gender: {gender}\n"
                f"Dwelling place: {dwelling_place}\n"
                f"Hobbies: {hobbies}\n"
                f"Diet: {diet}\n"
                f"Email: {email}\n")
        msg = MIMEMultipart()
        msg['From'] = os.getenv('EMAIL_ADDRESS')
        msg['To'] = os.getenv('RECEIVER_EMAIL')
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASS'))
            smtp.send_message(msg)
