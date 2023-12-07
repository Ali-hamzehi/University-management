from celery import shared_task
from django.core.mail import send_mail


@shared_task
def Send_change_password_email(email, token):
    subject = 'Password Change Request'
    message = f'Click the following link to change your password: http://127.0.0.1:8000/users/change-password-action/{token}/'
    sender_email = 'your_valid_email@example.com'
    send_mail(subject, message, sender_email, [email])