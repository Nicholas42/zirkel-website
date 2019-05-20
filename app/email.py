from app import mail
from flask_mail import Message


def send_mail(subject, content, recipients, sender="zirkel@nicholas-schwab.de"):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = content
    mail.send(msg)
