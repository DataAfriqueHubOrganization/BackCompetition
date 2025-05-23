import uuid
from django.db import models
from apps.auth_user.models import Country, TimeStampedModel, Users

class Team(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    members = models.ManyToManyField('auth_user.Users', related_name="teams")
    leader = models.ForeignKey(
        'auth_user.Users',
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="led_teams"
    )  # Leader de l'équipe

    def __str__(self):
        return self.name
class TeamJoinRequest(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="join_requests")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="join_requests")
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    #invitation ou demande
    team_join_request_status = models.CharField(max_length=20, choices=[('invitation', 'Invitation'), ('demande', 'Demande')], default='invitation')

    def __str__(self):
        return self.user.username + " - " + self.team.name
