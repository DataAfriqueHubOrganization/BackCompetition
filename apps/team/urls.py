from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
    path("", ListOrCreateTeam.as_view(), name="list_or_create_team"),
    path("<uuid:pk>", TeamDetail.as_view(), name="team_detail"),
    path("join-request/<uuid:pk>/update/", UpdateTeamRequestStatus.as_view(), name='update-team-request'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

