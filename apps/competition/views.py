from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .models import Challenge, Competition, CompetitionPhase
from .serializers import ChallengeSerializer, CompetitionSerializer, CompetitionPhaseSerializer
from ..competition.permissions import IsAdminOrReadOnly

###################################################################################
#                                   CHALLENGE                                      #
###################################################################################

class ChallengeListCreateView(APIView):
    """
    GET : Lister tous les challenges.
    POST : Créer un nouveau challenge (admin uniquement).
    """
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(
        operation_description="Récupère la liste de tous les challenges.",
        responses={200: ChallengeSerializer(many=True)}
    )
    def get(self, request):
        challenges = Challenge.objects.all()
        serializer = ChallengeSerializer(challenges, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Crée un nouveau challenge (admin uniquement).",
        request_body=ChallengeSerializer,
        responses={201: ChallengeSerializer, 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = ChallengeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ChallengeDetailView(APIView):
    """
    GET : Récupère un challenge par ID.
    """
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Challenge, pk=pk)

    @swagger_auto_schema(
        operation_description="Récupère un challenge par son ID.",
        responses={200: ChallengeSerializer, 404: 'Not Found'}
    )
    def get(self, request, pk):
        challenge = self.get_object(pk)
        serializer = ChallengeSerializer(challenge)
        return Response(serializer.data)


###################################################################################
#                                   COMPETITION                                   #
###################################################################################

class CompetitionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les compétitions.
    """
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = [IsAdminOrReadOnly]

    # Swagger s'auto-génère pour ModelViewSet


###################################################################################
#                             COMPETITIONS PHASES                                 #
###################################################################################

class CompetitionPhaseViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les phases de compétition.
    """
    queryset = CompetitionPhase.objects.all()
    serializer_class = CompetitionPhaseSerializer
    permission_classes = [IsAdminOrReadOnly]

    # Swagger s'auto-génère pour ModelViewSet
