from django.db import models
import uuid
from django.utils import timezone
from apps.dataset.models import  Dataset
from apps.partner.models import Partner
# Create your models here.
from back_datatour.models import  TimeStampedModel

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