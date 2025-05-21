# Create your models here.
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
def user_image_upload_path(instance, filename):
    return f'images_folder/user/{filename}'



class Users(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.ImageField(upload_to=user_image_upload_path, blank=True, null=True)
    user_image = models.ImageField(upload_to="users/", blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=10,
        choices=[("m", "m"), ("f", "f")],
        blank=True,
        null=True
    )
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name="country")
    residence_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True,
                                          related_name="resident")
    # logo = models.ImageField(upload_to="logos/", null=True, blank=True)  # Stocke les logos dans le dossier "logos/"
    profession = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=50, null=True)
    is_admin = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=64, unique=True, blank=True, null=True)

    def generate_verification_token(self):
        self.verification_token = get_random_string(64)
        self.save()