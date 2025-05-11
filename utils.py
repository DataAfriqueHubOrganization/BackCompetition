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
    
    

def send_team_creation_emails(team_name, members, leader):
    subject = f"Nouvelle équipe créée : {team_name}"
    for member in members:
        message = (
            f"Bonjour {member.username},\n\n"
            f"Vous avez été ajouté à l'équipe '{team_name}'.\n"
            f"Leader de l'équipe : {leader.username}\n\n"
            "Merci de confirmer votre participation et bonne chance pour la compétition !"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [member.email],
            fail_silently=False,
        )