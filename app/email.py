from flask import render_template

from app import mail
from flask_mail import Message


def send_mail(subject, content, recipients, sender="zirkel@nicholas-schwab.de"):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = content
    mail.send(msg)


def send_password_reset(user):
    token = user.get_reset_password_token()
    send_mail("Passwort-Reset", render_template("email/forgot_password.txt", token=token, user=user), [user.email])
