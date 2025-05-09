from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.team.models import Team, TeamJoinRequest
from utils import send_emails
from apps.competition.models import CompetitionParticipant

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
        

# @receiver(post_save, sender=Team)
# def handle_team_creation(sender, instance, created, **kwargs):
#     if created:
#         leader = instance.leader
#         members = instance.members.all()

#         # Ajouter directement le leader comme participant
#         CompetitionParticipant.objects.create(
#             user=leader,
#             competition=instance.competition,
#             team=instance,
#             has_accepted=True
#         )

#         for member in members:
#             if member != leader:
#                 # Créer une demande de jointure pour chaque membre (sauf leader)
#                 TeamJoinRequest.objects.get_or_create(team=instance, user=member)
