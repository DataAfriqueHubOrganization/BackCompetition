# views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Dataset, DatasetFile
# Importer tous les serializers nécessaires
from .serializers import (
    DatasetSerializer,
    DatasetFileSerializer, # Pour la réponse de certaines actions
    DatasetFileCreateSerializer,
    DatasetFileUpdateSerializer
)

class DatasetViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les Datasets.
    - Création initiale possible avec fichiers via le champ 'initial_files'.
    - Actions dédiées pour ajouter, mettre à jour (metadata), et supprimer des fichiers.
    """
    queryset = Dataset.objects.prefetch_related('files').all()
    # Serializer principal pour list/retrieve/create/update(dataset fields only)
    serializer_class = DatasetSerializer
    parser_classes = [MultiPartParser, FormParser] # Nécessaire pour 'initial_files' et 'add_file'

    def get_permissions(self):
        """ Admins pour toutes les modifications """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'add_file', 'update_file', 'delete_file']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    # --- Actions standard (ajustées) ---

    @swagger_auto_schema(
        operation_description="Crée un dataset, potentiellement avec des fichiers initiaux via 'initial_files' (Admin requis).",
        request_body=DatasetSerializer # Utilise le serializer principal
    )
    def create(self, request, *args, **kwargs):
        # La logique est dans DatasetSerializer.create
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Met à jour nom/description du dataset. Ignore 'initial_files'. (Admin requis)",
        request_body=openapi.Schema( # Définir explicitement pour la clarté de Swagger
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    def update(self, request, *args, **kwargs):
        # La logique est dans DatasetSerializer.update (ignore les fichiers)
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Met à jour partiellement nom/description du dataset. Ignore 'initial_files'. (Admin requis)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    def partial_update(self, request, *args, **kwargs):
        # La logique est dans DatasetSerializer.update (ignore les fichiers)
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Supprime un dataset et ses fichiers (Admin requis).")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # --- Actions personnalisées pour les fichiers ---

    @swagger_auto_schema(
        method='post',
        operation_description="Ajoute UN fichier à un dataset existant (Admin requis).",
        request_body=DatasetFileCreateSerializer, # Utilise le serializer dédié à la création
        responses={201: DatasetFileSerializer} # Retourne le fichier créé (format lecture)
    )
    @action(detail=True, methods=['post'], serializer_class=DatasetFileCreateSerializer, url_path='add-file')
    def add_file(self, request, pk=None):
        dataset = self.get_object()
        serializer = self.get_serializer(data=request.data) # Valide avec DatasetFileCreateSerializer
        serializer.is_valid(raise_exception=True)

        try:
            # Créer en passant les données validées et le dataset parent
            dataset_file = DatasetFile.objects.create(
                dataset=dataset,
                **serializer.validated_data
            )
            # Retourner les données formatées pour la lecture
            read_serializer = DatasetFileSerializer(dataset_file, context=self.get_serializer_context())
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='patch',
        operation_description="Met à jour les métadonnées (type, description) d'un fichier spécifique (Admin requis).",
        request_body=DatasetFileUpdateSerializer, # Utilise le serializer dédié à la MàJ metadata
        responses={200: DatasetFileSerializer} # Retourne le fichier mis à jour (format lecture)
    )
    @action(detail=True, methods=['patch'], serializer_class=DatasetFileUpdateSerializer, url_path='files/(?P<file_pk>[^/.]+)')
    def update_file(self, request, pk=None, file_pk=None):
        dataset = self.get_object()
        dataset_file = get_object_or_404(DatasetFile, pk=file_pk, dataset=dataset)

        # Valider les données reçues (uniquement type/description) avec le serializer de MàJ
        # Important: passer l'instance et partial=True pour permettre la MàJ partielle
        serializer = self.get_serializer(dataset_file, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save() # Sauvegarde les modifications sur l'instance dataset_file

        # Retourner les données formatées pour la lecture
        read_serializer = DatasetFileSerializer(dataset_file, context=self.get_serializer_context())
        return Response(read_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='delete',
        operation_description="Supprime UN fichier spécifique (Admin requis).",
        responses={204: "Fichier supprimé", 404: "Dataset ou Fichier non trouvé"}
    )
    @action(detail=True, methods=['delete'], url_path='files/(?P<file_pk>[^/.]+)')
    def delete_file(self, request, pk=None, file_pk=None):
        dataset = self.get_object()
        dataset_file = get_object_or_404(DatasetFile, pk=file_pk, dataset=dataset)
        dataset_file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)