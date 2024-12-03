from flask import render_template
from flask_mail import Message
from app import mail
from flask import current_app


def send_welcome_email(user):
    subject = "Üdvözöljük a BoxNinja-nál!"
    recipients = [user.email]
    html_body = render_template(
        "email/welcome.html", user=user, base_url="http://localhost:3000"
    )
    send_email(subject, recipients, html_body)


def send_login_notification(user, login_date, login_ip, login_device):
    subject = "Új bejelentkezés észlelve"
    recipients = [user.email]
    html_body = render_template(
        "email/login_notification.html",
        user=user,
        login_date=login_date,
        login_ip=login_ip,
        login_device=login_device,
        base_url="http://localhost:3000",
    )
    send_email(subject, recipients, html_body)


def send_delivery_notification(user, tracking_number):
    subject = "Csomagja megérkezett a BoxNinja-hoz"
    recipients = [user.email]
    html_body = render_template(
        "email/delivery_notification.html",
        user=user,
        tracking_number=tracking_number,
        base_url="http://localhost:3000",
    )
    send_email(subject, recipients, html_body)


def send_email(subject, recipients, html_body):
    msg = Message(
        subject, sender=current_app.config["MAIL_DEFAULT_SENDER"], recipients=recipients
    )
    msg.html = html_body
    mail.send(msg)
