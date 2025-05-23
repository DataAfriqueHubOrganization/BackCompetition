import uuid

from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Country(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

# class Users(AbstractUser):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# #     first_name = models.CharField(max_length=50)
# #     last_name = models.CharField(max_length=50)
# #     gender = models.CharField(
# #         max_length=10,
# #         choices=[("m", "m"), ("f", "f")],
# #         blank=True,
# #         null=True
# #     )
# #     country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name="country")
# #     residence_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True,
# #                                           related_name="resident")
# #     # logo = models.ImageField(upload_to="logos/", null=True, blank=True)  # Stocke les logos dans le dossier "logos/"
# #     profession = models.CharField(max_length=255, null=True)
# #     phone = models.CharField(max_length=50, null=True)
# #     is_admin = models.BooleanField(default=False)
# #     status = models.BooleanField(default=True)
# #     updated_at = models.DateTimeField(auto_now=True)
# #     is_verified = models.BooleanField(default=False)
# #     verification_token = models.CharField(max_length=64, unique=True, blank=True, null=True)

# #     def generate_verification_token(self):
# #         self.verification_token = get_random_string(64)
# #         self.save()

# class Team(TimeStampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255)
#     country = models.ForeignKey(Country, on_delete=models.PROTECT)
#     members = models.ManyToManyField(Users, related_name="teams")
#     leader = models.ForeignKey(
#         Users,
#         on_delete=models.PROTECT,
#         null=True, blank=True,
#         related_name="led_teams"
#     )  # Leader de l'équipe


# class Partner(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     logo = models.ImageField(upload_to='static/partners/', null=True, blank=True)
#     website_url = models.URLField(null=True, blank=True)

# class Competition(TimeStampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     Statut_choice = [
#         ('Comming soon', 'COMMING SOON'),
#         ('Registration', 'REGISTRATION'),
#         ('Ongoing', 'ONGOING'),
#         ('Closed', 'CLOSED'),
#     ]
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     status = models.CharField(
#         max_length=15,
#         choices=Statut_choice,
#         blank=True,
#         null=True
#     )
#     inscription_start = models.DateTimeField()
#     inscription_end = models.DateTimeField()
#     # price
#     partners = models.ManyToManyField(Partner, related_name="partner")


# class CompetitionPhase(TimeStampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()
#     @property
#     def is_finished(self):
#         return timezone.now() > self.end_date

#     def __str__(self):
#         return self.name

# class Leaderboard(TimeStampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     team = models.ForeignKey(Team, on_delete=models.CASCADE)
#     competition_phase = models.ForeignKey(CompetitionPhase, on_delete=models.CASCADE)
#     private_score = models.DecimalField(max_digits=20, decimal_places=10)
#     public_score = models.DecimalField(max_digits=20, decimal_places=10)
#     rank = models.PositiveIntegerField()

# class DatasetFile(TimeStampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     dataseturl = models.CharField(max_length=255)
#     description = models.JSONField()
# class Dataset(TimeStampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     Dataset_file = models.ManyToManyField(DatasetFile, related_name ="dataset")
  

# class Challenge(TimeStampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255)
#     # description = models.TextField()
#     description  = models.JSONField(default = dict) ## on stcokera un json
#     competition_phase = models.ForeignKey(CompetitionPhase, on_delete=models.CASCADE)
#     dataset_urls = models.ManyToManyField(Dataset, related_name="dataset")
#     def is_active(self):
#         return not self.competition_phase.is_finished

#     def __str__(self):
#         return self.name

# class Submission(TimeStampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="submissions")
#     challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="submissions")
#     file = models.FileField(upload_to="static/submissions/")
#     score = models.FloatField(null=True, blank=True)


# class Comment(TimeStampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     users = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_comment")
#     competition_phase = models.ForeignKey(CompetitionPhase, on_delete=models.CASCADE, related_name="competition_phase")
#     content = models.TextField()


# class Announcement(TimeStampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     users = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_announcement")
#     name = models.CharField(max_length=255)
#     description = models.TextField()
