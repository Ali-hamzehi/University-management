from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_approval_email(student_email):
    """
    Sends an approval email to the specified student email.

    Args:
        student_email (str): The email address of the student.

    Returns:
        None
    """
    subject = 'Substitution Form Approved'
    message = 'Your substitution form has been approved. Please check your schedule.'
    send_mail(subject, message, 'example@example.com', [student_email])


@shared_task
def send_rejection_email(student_email):
    """
    Sends a rejection email to a student.

    Args:
        student_email (str): The email address of the student.

    Returns:
        None
    """
    subject = 'Substitution Form Rejected'
    message = 'Unfortunately, your substitution form has been rejected.'
    send_mail(subject, message, 'example@example.com', [student_email])


@shared_task
def send_confirmed_email_removal_request(student_email):
    """
    Sends a confirmed removal request email to a student.

    Parameters:
        student_email (str): The email address of the student.

    Returns:
        None
    """
    subject = 'Confirmed Removal Request'
    message = 'Your request for removal has been approved.'
    send_mail(subject, message, 'example@example.com', [student_email])


@shared_task
def send_reject_email_removal_request(student_email):
    """
    Sends a rejection email for a removal request to the specified student email.

    Parameters:
        student_email (str): The email address of the student.

    Returns:
        None
    """
    subject = 'Rejected Removal Request'
    message = 'Your request for removal has been rejected.'
    send_mail(subject, message, 'example@example.com', [student_email])


@shared_task
def send_confirmed_email_ForBoysRequest(student_email):
    """
    Sends a confirmation email for a removal request to the specified student email address.

    Parameters:
        student_email (str): The email address of the student who made the removal request.

    Returns:
        None
    """
    subject = 'Confirmed Removal Request'
    message = 'Your request for removal has been approved.'
    send_mail(subject, message, 'example@example.com', [student_email])


@shared_task
def send_reject_email_ForBoysRequest(student_email):
    """
    Sends a rejection email for a removal request to the specified student email.

    Parameters:
        student_email (str): The email address of the student.

    Returns:
        None
    """
    subject = 'Rejected Removal Request'
    message = 'Your request for removal has been rejected.'
    send_mail(subject, message, 'example@example.com', [student_email])

