from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(TimeStampedModel):
    name = models.CharField(max_length=255)


class Users(AbstractUser):
    gender = models.CharField(
        max_length=10,
        choices=[("m", "m"), ("f", "f")],
        blank=True,
        null=True
    )
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name="country")
    residence_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True,
                                          related_name="resident")
    profession = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Team(TimeStampedModel):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    members = models.ManyToManyField(Users, related_name="teams")
    leader = models.ForeignKey(Users, on_delete=models.PROTECT, null=True, blank=True,
                               related_name="led_teams")  # Leader de l'équipe

    def clean(self):
        if self.pk and self.members.count() != 3:
            raise ValidationError("Une équipe doit avoir 3 membres.")
        if self.leader and self.leader not in self.members.all():
            raise ValidationError("Le leader doit faire partie des membres de l'équipe.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Sauvegarde d'abord pour pouvoir accéder aux membres
        if self.pk and self.members.count() != 3:
            raise ValidationError("Une équipe doit avoir au moins 3 membres.")
        if self.leader and self.leader not in self.members.all():
            raise ValidationError("Le leader doit faire partie des membres de l'équipe.")


class Partner(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


class Competition(TimeStampedModel):
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
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Leaderboard(TimeStampedModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    competition_phase = models.ForeignKey(CompetitionPhase, on_delete=models.CASCADE)
    private_score = models.DecimalField(max_digits=20, decimal_places=10)
    public_score = models.DecimalField(max_digits=20, decimal_places=10)
    rank = models.PositiveIntegerField()


class Dataset(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    dataset_url = models.CharField(max_length=255)


class Challenge(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    competition_phase = models.ForeignKey(CompetitionPhase, on_delete=models.CASCADE)
    dataset_urls = models.ManyToManyField(Dataset, related_name="dataset")


class Submission(TimeStampedModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="submissions")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="submissions")
    file = models.FileField(upload_to="static/submissions/")
    score = models.FloatField(null=True, blank=True)


class Comment(TimeStampedModel):
    users = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_comment")
    compétition_phase = models.ForeignKey(CompetitionPhase, on_delete=models.CASCADE, related_name="competition_phase")
    content = models.TextField()


class Announcement(TimeStampedModel):
    users = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_announcement")
    name = models.CharField(max_length=255)
    description = models.TextField()

############################################


# class Submission(models.Model):
#     team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="submissions")
#     challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="submissions")
#     file = models.FileField(upload_to="static/submissions/")
#     score = models.FloatField(null=True, blank=True)
#     submitted_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(
#         max_length=20, 
#         choices=[("pending", "Pending"), ("evaluated", "Evaluated")], 
#         default="pending"
#     )


# class Leaderboard(models.Model):
#     competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="leaderboards")
#     team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="leaderboard_entries")
#     phase = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="leaderboard_entries")
#     score = models.FloatField()
#     rank = models.IntegerField()


# # Modèle Annonce
# class Announcement(models.Model):


# # Modèle Commentaire
# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
#
#     content = models.TextField()

#     is_moderated = models.BooleanField(default=False)
