from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', CommentViewSet, basename='announcement')

urlpatterns = [
    
#     Endpoints pour Comment
    # path('', CommentListCreateAPIView.as_view(), name='comment-list'),
    # path('<uuid:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-detail'),
    # URL pour lister tous les commentaires et créer un commentaire
    path('', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    # URL pour récupérer, mettre à jour et supprimer un commentaire spécifique
    path('<uuid:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-retrieve-update-destroy'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

