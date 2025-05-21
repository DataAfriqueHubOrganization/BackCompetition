from django.db import models
import uuid

# def partner_logo_upload_path(instance, filename):
#     return f'images_folder/partner/{filename}'

def partner_logo_upload_path(instance, filename):
    safe_name = instance.name.replace(" ", "_").lower()
    return f'images_folder/partner/{safe_name}/{filename}'

class Partner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to=partner_logo_upload_path, blank=True, null=True)
    website_url = models.URLField(null=True, blank=True)
