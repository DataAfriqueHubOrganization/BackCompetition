from django.db import models
import uuid

class Partner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='static/partners/', null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
