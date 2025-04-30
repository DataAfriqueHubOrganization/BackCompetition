from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .models import Dataset
from .serializers import DatasetSerializer


###################################################################################
#                                 DATASETS                                        #
###################################################################################

class DatasetViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des datasets de compétition.
    Permet de lister, ajouter, mettre à jour et supprimer les datasets.
    """
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Liste tous les datasets disponibles.",
        responses={200: DatasetSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Uploader un nouveau dataset pour une compétition.",
        request_body=DatasetSerializer,
        responses={201: DatasetSerializer, 400: "Données invalides"}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Récupère les détails d’un dataset.",
        responses={200: DatasetSerializer, 404: "Non trouvé"}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Met à jour un dataset existant.",
        request_body=DatasetSerializer,
        responses={200: DatasetSerializer, 400: "Données invalides"}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Supprime un dataset.",
        responses={204: "Supprimé avec succès", 404: "Non trouvé"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
