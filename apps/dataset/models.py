from django.db import models

# Create your models here.
import uuid
from back_datatour.models import TimeStampedModel
import os
from django.utils.translation import gettext_lazy as _


def dataset_file_upload_path(instance, filename):
    """
    Les fichiers seront uploadés dans MEDIA_ROOT/datasets/<dataset_id>/<file_type>/<filename_original>
    Note: instance.dataset.id est disponible car l'objet DatasetFile est sauvegardé *après*
          que le Dataset ait été créé et que la relation ForeignKey soit établie (dans le serializer).
    """
    dataset_id = instance.dataset.id if instance.dataset else 'misc' # Précaution si dataset non défini
    file_type_folder = instance.get_file_type_display().lower().replace(' ', '_') # Ex: 'training_set'
    # Utiliser le nom de fichier original stocké pour le chemin final
    final_filename = instance.original_filename or filename
    return os.path.join('datasets', str(dataset_id), file_type_folder, final_filename)


class Dataset(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    #Dataset_file = models.ManyToManyField(DatasetFile, related_name ="dataset")
  
    def __str__(self):
        return self.name
    

class DatasetFile(TimeStampedModel):
    class FileType(models.TextChoices):
        TRAIN = 'TRAIN', _('Training Set')
        TEST = 'TEST', _('Test Set')
        SUBMISSION = 'SUBMISSION', _('Submission Example')
        SOLUTION = 'SOLUTION', _('Solution File') # Exemple de type additionnel
        OTHER = 'OTHER', _('Other')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset = models.ForeignKey(
        Dataset,
        related_name='files', # Permet d'accéder aux fichiers via dataset.files.all()
        on_delete=models.CASCADE, # Si le Dataset est supprimé, ses fichiers aussi
        null=True,  # <-- Add this temporarily
        blank=True
    )
    file = models.FileField(upload_to=dataset_file_upload_path)
    # Type de fichier défini explicitement
    file_type = models.CharField(
        max_length=20,
        choices=FileType.choices,
        default=FileType.OTHER,
    )
    original_filename = models.CharField(max_length=255, blank=True, editable=False)
    # Description optionnelle spécifique à ce fichier
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.dataset.name} - {self.get_file_type_display()} ({self.original_filename})"

    def save(self, *args, **kwargs):
        # Sauvegarder le nom original avant la première sauvegarde si non défini
        if not self.pk and self.file and not self.original_filename:
             self.original_filename = self.file.name
        # Si le fichier change, mettre à jour le nom original (important pour upload_to)
        # Note : Ceci peut être complexe si le fichier est modifié via l'admin sans réupload.
        # Simplification : on ne met à jour original_filename que lors de la création initiale.
        super().save(*args, **kwargs)

        # Important : Si le nom original change APRÈS la première sauvegarde,
        # l'ancien fichier pourrait ne pas être nettoyé correctement par upload_to seul.
        # django-cleanup gère mieux ce cas en se basant sur l'instance.