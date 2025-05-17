from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import CompetitionPhase, Competition
from django.conf import settings
import os


base_path = getattr(settings, "COMPETITION_FOLDER", "competitions")


@receiver(post_save, sender=CompetitionPhase)
def update_competition_inscription_end(sender, instance, **kwargs):
    competition = instance.competition
    last_phase = competition.competitionphase_set.order_by('-end_date').first()
    if last_phase and competition.inscription_end != last_phase.end_date:
        competition.inscription_end = last_phase.end_date
        competition.save(update_fields=['inscription_end'])



@receiver(post_save, sender=Competition)
def create_folder(sender, instance, created, **kwargs):
    """
    Crée un dossier pour la compétition après sa création.
    """
    if created:
        base_path = "competitions"
        folder_name = instance.name.replace(" ", "_").lower()
        folder_path = os.path.join(base_path, folder_name)
        os.makedirs(folder_path)
        print(f"Dossier créé : {folder_path}")
        
        
@receiver(pre_delete, sender=Competition)
def zip_competition_folder(sender, instance, created, **kwargs):
    base_path = "competitions"
    folder_name = instance.name.replace(" ", "_").lower()
    folder_path = os.path.join(base_path, folder_name)
    
    if os.path.exists(folder_path):
       zip_path = f"{folder_path}.zip"
       shutil.make_archive(folder_path, 'zip', folder_path)
       shutil.rmtree(folder_path)
       print("dossier zipper avec succès:{zip_path}")
    else:
        print(f"Dossier non trouvé : {folder_path}")
        
        
### COMPETION PHASE

@receiver(post_save, sender=CompetitionPhase)
def create_folder(sender, instance, created, **kwargs):
    """
    Crée un dossier pour la compétition après sa création.
    """
    if created:
        competition_name = instance.competition.name.replace(" ", "_").lower()
        phase_name = instance.name.replace(" ", "_").lower()
        base_path = os.path.join("competitions", competition_name)    
        folder_path = os.path.join(base_path, phase_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Dossier créé : {folder_path}")
        
        
@receiver(pre_delete, sender=CompetitionPhase)
def zip_competition_folder(sender, instance, created, **kwargs):
    competition_name = instance.competition.name.replace(" ", "_").lower()
    phase_name = instance.name.replace(" ", "_").lower()
    base_path = os.path.join("competitions", competition_name)    
    folder_path = os.path.join(base_path, phase_name)

    if os.path.exists(folder_path):
       zip_path = f"{folder_path}.zip"
       shutil.make_archive(folder_path, 'zip', folder_path)
       shutil.rmtree(folder_path)
       print("dossier zipper avec succès:{zip_path}")
    else:
        print(f"Dossier non trouvé : {folder_path}")
        
        
        
