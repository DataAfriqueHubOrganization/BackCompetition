from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CompetitionPhase

@receiver(post_save, sender=CompetitionPhase)
def update_competition_inscription_end(sender, instance, **kwargs):
    competition = instance.competition
    last_phase = competition.competitionphase_set.order_by('-end_date').first()
    if last_phase and competition.inscription_end != last_phase.end_date:
        competition.inscription_end = last_phase.end_date
        competition.save(update_fields=['inscription_end'])
