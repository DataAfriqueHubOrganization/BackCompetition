from django.db import models
import uuid

from apps.auth_user.models import Users
from back_datatour.models import Country, TimeStampedModel

class Team(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    members = models.ManyToManyField('auth_user.Users', related_name="teams")
    leader = models.ForeignKey(
        'auth_user.Users',
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="led_teams"
    )  # Leader de l'équipe


class TeamJoinRequest(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="join_requests")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="join_requests")
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

