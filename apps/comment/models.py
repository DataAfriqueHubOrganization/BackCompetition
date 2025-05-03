from django.db import models
import uuid
from apps.auth_user.models import Users
from apps.competition.models import CompetitionPhase
from back_datatour.models import TimeStampedModel


class Comment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth_user.Users', on_delete=models.CASCADE, related_name="user_comment")
    competition_phase = models.ForeignKey(CompetitionPhase, on_delete=models.CASCADE, related_name="competition_phase")
    content = models.TextField()

