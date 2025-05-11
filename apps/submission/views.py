from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema

from .models import Submission, Leaderboard
from .serializers import SubmissionSerializer, LeaderboardSerializer


###################################################################################
#                                SUBMISSION                                       #
###################################################################################

class SubmissionViewSet(viewsets.ModelViewSet):
    """
    Permet de gérer les soumissions des participants à une compétition.
    """
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Submission.objects.all()

    @swagger_auto_schema(
        operation_description="Uploader une soumission à une compétition.",
        request_body=SubmissionSerializer,
        responses={
            201: "Soumission enregistrée avec succès.",
            400: "Données invalides."
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


###################################################################################
#                                LEADERBOARD                                      #
###################################################################################

class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    Affiche et met à jour les scores des participants à une compétition.
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    permission_classes = [permissions.AllowAny]
