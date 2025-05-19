from django.db import models
import uuid
from apps.competition.models import Challenge
from apps.team.models import Team
from apps.competition.models import CompetitionPhase
from apps.auth_user.models import  TimeStampedModel


#creation de score 
# class Score(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     # submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="scores")
#     score = models.FloatField()
#     # public_score = models.FloatField()
#     created_at = models.DateTimeField(auto_now_add=True)

class Submission(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="submissions")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="submissions")
    file = models.FileField(upload_to="static/submissions/")
    score = models.FloatField()
    # score = models.ForeignKey(Score, on_delete=models.CASCADE, related_name="scores")
    limit = models.IntegerField(default=5)

# to remove!!!!!!!!!!!
# class Leaderboard(TimeStampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     team = models.ForeignKey(Team, on_delete=models.CASCADE)
#     competition_phase = models.ForeignKey(CompetitionPhase, on_delete=models.CASCADE)
#     rank = models.PositiveIntegerField()
