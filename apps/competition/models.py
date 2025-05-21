from django.db import models
import uuid
from django.utils import timezone
from apps.dataset.models import  DatasetFile, Dataset
from apps.partner.models import Partner
# Create your models here.
from apps.auth_user.models import  TimeStampedModel
from django.conf import settings
from apps.team.models import Team
from django.core.exceptions import ValidationError


"""""
le statut de competion change de:
comming soon à registration  sssi today == date de debut inscription; Competition
de registration à ongoing si today == date de debut de la phase nationale; CompetitionPhase
de ongoing à closed si today == date de fin de la phase internationale; CompetitionPhase
inscription_start
on verifie si c'est nationla ou non puis on tag start_date
"""

def competition_image_upload_path(instance, filename):
    return f'images_folder/competition/{instance.id}/{filename}'

class Competition(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition_image = models.ImageField(upload_to=competition_image_upload_path,blank=True, null=True)
    Statut_choice = [
        ('Comming soon', 'COMMING SOON'),
        ('Registration', 'REGISTRATION'),
        ('Ongoing', 'ONGOING'),
        ('Closed', 'CLOSED'),
    ]
    name = models.CharField(max_length=255, unique=True)
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
    PHASE_CHOICES = (
        ('national', 'National'),
        ('international', 'International'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, choices=PHASE_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

##### mettre des message erreur parlant!
    def clean (self):
        super().clean()
        if self.name == 'international':
            phase_national = CompetitionPhase.objects.filter(competition=self.competition, name='national').first()
            if not phase_national:
                raise ValidationError("La phase nationale doit exister avant de créer une phase internationale.")
            
            if phase_national.end_date >= self.start_date:
                raise ValidationError({"phase":"La date de début de la phase internationale doit être après la date de fin de la phase nationale."})

        # Vérification de la validité des dates
        if self.start_date >= self.end_date:
            raise ValidationError("La date de début doit être antérieure à la date de fin.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
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
    dataset_urls = models.ManyToManyField(DatasetFile, related_name="datasetfile")
    metric = models.CharField(max_length=255, blank=True, null=True)
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
