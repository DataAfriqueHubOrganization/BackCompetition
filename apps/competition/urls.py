from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# Initialiser le router
router = DefaultRouter()
router.register(r'competitions', CompetitionViewSet)
router.register(r'phases', CompetitionPhaseViewSet)



urlpatterns = [

#     ## challenge
    path('challenges/', ChallengeListCreateView.as_view(), name='challenge-list-create'),
    path('challenges/<uuid:pk>/', ChallengeDetailView.as_view(), name='challenge-detail'),
    path('', include(router.urls)),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

