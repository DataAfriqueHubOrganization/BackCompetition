from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from apps.team.models import Team, TeamJoinRequest
from utils import send_emails
# from apps.competition.models import CompetitionParticipant
from apps.submission.models import Submission
import os
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


### TEAM

@receiver(post_save, sender=Submission)
def create_folder(sender, instance, created, **kwargs):
    """
    Crée un dossier pour la compétition après sa création.
    """
    if created:
        competition_name = instance.challenge.competition_phase.competition.replace(" ", "_").lower()
        phase_name = instance.challenge.competition_phase.replace(" ", "_").lower()
        team_name = instance.team.name.replace(" ", "_").lower()
        base_path = os.path.join("competitions", competition_name, phase_name)    
        folder_path = os.path.join(base_path, team_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Dossier créé : {folder_path}")
        
        
@receiver(pre_delete, sender=Submission)
def zip_competition_folder(sender, instance, created, **kwargs):
    competition_name = instance.challenge.competition_phase.competition.replace(" ", "_").lower()
    phase_name = instance.challenge.competition_phase.replace(" ", "_").lower()
    team_name = instance.team.name.replace(" ", "_").lower()
    base_path = os.path.join("competitions", competition_name, phase_name)    
    folder_path = os.path.join(base_path, team_name)

    if os.path.exists(folder_path):
       zip_path = f"{folder_path}.zip"
       shutil.make_archive(folder_path, 'zip', folder_path)
       shutil.rmtree(folder_path)
       print("dossier zipper avec succès:{zip_path}")
    else:
        print(f"Dossier non trouvé : {folder_path}")        