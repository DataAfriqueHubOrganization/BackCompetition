from django.urls import path, include
from back_datatour.views import UserRegister
from rest_framework.routers import DefaultRouter
from .views import CompetitionViewSet, CompetitionPhaseViewSet

# Initialiser le router
router = DefaultRouter()
router.register(r'competitions', CompetitionViewSet)
router.register(r'phases', CompetitionPhaseViewSet)

urlpatterns = [
    # Route existante
    path("register/", UserRegister.as_view(), name='users_register'),
    
    # Routes API
    path('', include(router.urls)),  # Notez que j'ai supprimé 'api/' ici
]