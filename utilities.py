import random
from flask_mail import Mail, Message

mail = Mail()

def send_otp(app, email, otp):
    with app.app_context():
        msg = Message('Verification Token', sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = f'Your verification token is {otp}'
        mail.send(msg)
