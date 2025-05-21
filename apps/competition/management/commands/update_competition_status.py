from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.competition.models import Competition, CompetitionPhase
from django.db.models import Q

"""""
le statut de competion change de:
comming soon à registration  sssi today == date de debut inscription ;Competition
de registration à ongoing si today == date de debut de la phase nationale; CompetitionPhase
de ongoing à closed si today == date de fin de la phase internationale; CompetitionPhase
inscription_start
on verifie si c'est nationla ou non puis on tag start_date
"""

class Command(BaseCommand):
    help = 'Update the status of competitions and competition phases based on the current date'

    def handle(self, *args, **kwargs):
        # Update Competition status
        now = timezone.now()
        competitions = Competition.objects.all()
        for competition in competitions:
            if competition.inscription_start > now:
                competition.status = 'Coming soon'
            elif competition.inscription_start <= now < competition.inscription_end:
                competition.status = 'Registration'
            elif CompetitionPhase.objects.filter(competition=competition, phase_type='national', start_date__lte=now).exists():
                # Si la phase nationale a commencé
                competition.status = 'Ongoing'
            elif CompetitionPhase.objects.filter(competition=competition, phase_type='international', end_date__lt=now).exists():
                # Si la phase internationale est terminée
                competition.status = 'Closed'
            competition.save()
            
            
            
            # Pour structurer un cron job dans un projet Django, il est courant d'utiliser une tâche planifiée qui exécute une commande de management Django à intervalles réguliers.
            # Voici les étapes générales :

            # 1. Créez une commande de management (ce que vous avez déjà fait).
            # 2. Ajoutez une tâche cron sur le serveur pour exécuter cette commande périodiquement.

            # Exemple de ligne à ajouter dans la crontab (utilisez `crontab -e` pour éditer) :
            # Ici, la commande sera exécutée tous les jours à minuit.

            # 0 0 * * * /path/to/your/venv/bin/python /home/user/Bureau/FATOU\ FALL/2.PROJET/4.Data\ Afrique\ hub/BackCompetition/manage.py update_competition_status

            # Assurez-vous d'utiliser le chemin correct vers votre environnement virtuel Python et le fichier manage.py.
            # Vous pouvez vérifier que la commande fonctionne en l'exécutant manuellement :
            # python manage.py update_competition_status

            # Pour des tâches plus complexes ou une gestion avancée, vous pouvez aussi utiliser des packages comme django-celery-beat.
                       
            # Pour exécuter la commande toutes les minutes, ajoutez cette ligne à votre crontab :
            # * * * * * /path/to/your/venv/bin/python /home/user/Bureau/FATOU\ FALL/2.PROJET/4.Data\ Afrique\ hub/BackCompetition/manage.py update_competition_status
            # Cela lancera la commande chaque minute. Adaptez le chemin de l'environnement virtuel et du manage.py selon votre configuration.
            # Exemple de chemin pour votre environnement virtuel :
            # /home/user/Bureau/FATOU FALL/2.PROJET/4.Data Afrique hub/BackCompetition/venv/bin/python