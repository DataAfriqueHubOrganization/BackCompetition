from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.team.models import Team, TeamJoinRequest
from utils import send_emails

@receiver(post_save, sender=TeamJoinRequest)
def update_competition_join(sender, instance, **kwargs):
    if instance.status=="accepted":
        team = instance.team
        user = instance.user
        # Add the user to the team members
        team.members.add(user)
        send_emails(
            subject="Team Join Request Accepted",
            message=f"Hello {user.username}, your request to join the team {team.name} has been accepted.",
            recipient_list=[user.email]
        )
        
