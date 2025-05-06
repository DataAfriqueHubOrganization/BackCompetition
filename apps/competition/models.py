from django.db import models
import uuid
from django.utils import timezone
from apps.dataset.models import  Dataset
from apps.partner.models import Partner
# Create your models here.
from apps.auth_user.models import  TimeStampedModel
from django.conf import settings
from apps.team.models import Team

class Competition(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Statut_choice = [
        ('Comming soon', 'COMMING SOON'),
        ('Registration', 'REGISTRATION'),
        ('Ongoing', 'ONGOING'),
        ('Closed', 'CLOSED'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=15,
        choices=Statut_choice,
        blank=True,
        null=True
    )
    inscription_start = models.DateTimeField()
    inscription_end = models.DateTimeField()
    # price
    partners = models.ManyToManyField(Partner, related_name="partner")

    @property
    def inscription_finished(self):
        return timezone.now() > self.inscription_end
    @property
    def inscription_not_started(self):
        return timezone.now() < self.inscription_start
    def __str__(self):
        return self.name
class CompetitionPhase(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    @property
    def is_finished(self):
        return timezone.now() > self.end_date

    def __str__(self):
        return self.name

class Challenge(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    # description = models.TextField()
    description  = models.JSONField(default = dict) ## on stcokera un json
    competition_phase = models.ForeignKey(CompetitionPhase, on_delete=models.CASCADE)
    dataset_urls = models.ManyToManyField(Dataset, related_name="dataset")
    def is_active(self):
        return not self.competition_phase.is_finished

    def __str__(self):
        return self.name
    
class CompetitionParticipant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'competition')  # Empêche les participations en double
