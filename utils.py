from flask import render_template, url_for
from flask_mail import Message
from threading import Thread
from app import app, mail


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            app.logger.error(f"Failed to send email: {str(e)}")


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    
    # Send email asynchronously
    if app.config['TESTING']:
        mail.send(msg)
    else:
        Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.generate_reset_token()
    send_email(
        'Reset Your Password',
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt',
                                 user=user, token=token),
        html_body=render_template('email/reset_password.html',
                                 user=user, token=token)
    )


def format_duration(seconds):
    """Format seconds into a HH:MM:SS string"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


def calculate_grade(percentage):
    """Return a letter grade based on percentage"""
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C" 
    elif percentage >= 50:
        return "D"
    else:
        return "F"
