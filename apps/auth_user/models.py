from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
import uuid
from back_datatour.models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class Users(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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