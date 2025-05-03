from django.db import models
import uuid
from apps.auth_user.models import Users
from back_datatour.models import  TimeStampedModel

class Announcement(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth_user.Users', on_delete=models.CASCADE, related_name="user_announcement")
    name = models.CharField(max_length=255)
    description = models.TextField()
