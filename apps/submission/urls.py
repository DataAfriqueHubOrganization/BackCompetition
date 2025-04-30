from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# Initialiser le router
router = DefaultRouter()
router.register(r'leaderboards', LeaderboardViewSet)
router.register(r'submissions', SubmissionViewSet, basename='submission')



urlpatterns = [
    
    path('', include(router.urls)),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

