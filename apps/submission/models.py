from django.db import models
import uuid
from apps.competition.models import Challenge
from apps.team.models import Team
from apps.competition.models import CompetitionPhase
from apps.auth_user.models import  TimeStampedModel

class Submission(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="submissions")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="submissions")
    file = models.FileField(upload_to="static/submissions/")
    score = models.FloatField(null=True, blank=True)


class Leaderboard(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    competition_phase = models.ForeignKey(CompetitionPhase, on_delete=models.CASCADE)
    private_score = models.DecimalField(max_digits=20, decimal_places=10)
    public_score = models.DecimalField(max_digits=20, decimal_places=10)
    rank = models.PositiveIntegerField()
