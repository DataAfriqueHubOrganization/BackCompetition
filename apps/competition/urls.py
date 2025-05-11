from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

### Competition
    path('', CompetitionListCreate.as_view(), name='competition-list-create'),
    path('<uuid:pk>/', CompetitionDetail.as_view(), name='competition-detail'),

### Competition phase
    path('phases/', CompetitionPhaseListCreate.as_view(), name='competition-phase-list-create'),
    path('phase/<uuid:pk>/', CompetitionPhaseDetail.as_view(), name='competition-phase-detail'),

### challenge
    path('challenges/', ChallengeListCreate.as_view(), name='challenge-list-create'),
    path('challenge/<uuid:pk>/', ChallengeDetail.as_view(), name='challenge-detail'),
### competition participant
    path('<uuid:competition_id>/participate/', ParticipateInCompetition.as_view(), name='participate-in-competition'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

