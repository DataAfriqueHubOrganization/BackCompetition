from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly
from .models import Comment
from apps.comment.serializers import CommentSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.auth_user.permissions import *
from rest_framework import viewsets


class CommentViewSet(viewsets.ModelViewSet):
    """
    GET : Liste tous les commentaires.
    POST : Crée un nouveau commentaire (seulement pour les utilisateurs authentifiés).
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        """ Assigns permissions based on action. """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """ Set the user of the comment to the logged-in user. """
        # Le serializer ici sera CommentSerializer (grâce à get_serializer_class)
        # Il contient competition_phase et content dans validated_data
        serializer.save(user=self.request.user)

    # --- Swagger documentation (ajustée pour request_body de update/patch) ---
    @swagger_auto_schema(
        operation_description="Lister tous les commentaires.",
        responses={200: CommentSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        """
        Cette méthode permet à tout le monde de voir les commentaires.
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new comment...",
        request_body=CommentSerializer, # Input utilise CommentSerializer
        responses={201: CommentSerializer} # Réponse utilise CommentSerializer
    )
    def post(self, request, *args, **kwargs):
        """
        Permet uniquement à un utilisateur authentifié de créer un commentaire.
        """
        # Vérifie si l'utilisateur est authentifié (c'est en fait fait par la permission IsAuthenticatedOrReadOnly)
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Vous devez être connecté pour créer un commentaire."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Vérifier que le contenu du commentaire n'est pas vide
        content = request.data.get("content", "").strip()
        if not content:
            return Response(
                {"detail": "Le contenu du commentaire ne peut pas être vide."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().post(request, *args, **kwargs)



class CommentRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsOwnerOrAdmin]  # Permet uniquement aux auteurs ou admins de modifier/supprimer.

    def get_object(self, pk):
        return get_object_or_404(Comment, pk=pk)

    def get(self, request, pk):
        # Récupérer un commentaire, accessible à tous, même non authentifiés.
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk):
        # Permet la mise à jour du commentaire uniquement à l'auteur ou à l'admin.
        comment = self.get_object(pk)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        # Permet la mise à jour partielle uniquement à l'auteur ou à l'admin.
        comment = self.get_object(pk)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Permet la suppression uniquement à l'auteur ou à l'admin.
        comment = self.get_object(pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
