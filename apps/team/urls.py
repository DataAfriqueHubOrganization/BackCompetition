from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [

    path("", ListOrCreateTeam.as_view(), name="list_or_create_teams"),
    path("<uuid:pk>", TeamDetail.as_view(), name="team_detail"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

