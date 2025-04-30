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




