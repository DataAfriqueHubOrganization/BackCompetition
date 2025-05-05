from django.core.mail import send_mail

from django.conf import settings
def send_emails(subject, message, recipient_list):
    """
        Function to send an email using Django's send_mail function.
    """
    
    if not isinstance(recipient_list, list):
        raise ValueError("recipient_list must be a list of email addresses.")
        
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )