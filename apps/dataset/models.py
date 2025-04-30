from django.db import models

# Create your models here.
import uuid
from back_datatour.models import TimeStampedModel

class DatasetFile(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataseturl = models.CharField(max_length=255)
    description = models.JSONField()

class Dataset(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    Dataset_file = models.ManyToManyField(DatasetFile, related_name ="dataset")
  

