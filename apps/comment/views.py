from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS

from .models import Comment
from apps.comment.serializers import CommentSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Autorisation personnalisée : Propriétaire ou Admin
class IsOwnerOrAdmin(BasePermission):
    """
    Autorise la modification ou la suppression seulement si l'utilisateur est
    le propriétaire (champ 'users') ou un administrateur.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.users == request.user or request.user.is_staff or request.user.is_superuser


###################################################################################
#                                   COMMENT                                       #
###################################################################################

class CommentListCreateAPIView(generics.ListCreateAPIView):
    """
    GET : Liste tous les commentaires.
    POST : Crée un nouveau commentaire.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Lister tous les commentaires ou en créer un nouveau.",
        responses={200: CommentSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Créer un nouveau commentaire.",
        request_body=CommentSerializer,
        responses={201: CommentSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET : Récupère un commentaire par son ID.
    PUT/PATCH : Met à jour un commentaire (propriétaire ou admin).
    DELETE : Supprime un commentaire (propriétaire ou admin).
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    @swagger_auto_schema(
        operation_description="Récupère un commentaire spécifique par ID.",
        responses={200: CommentSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Met à jour un commentaire existant.",
        request_body=CommentSerializer,
        responses={200: CommentSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partiellement met à jour un commentaire existant.",
        request_body=CommentSerializer,
        responses={200: CommentSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Supprime un commentaire existant.",
        responses={204: 'No content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
