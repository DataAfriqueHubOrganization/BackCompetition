from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from .models import Team
from .serializers import TeamSerializer


###################################################################################
#                                   TEAM                                          #
###################################################################################

class ListOrCreateTeam(APIView):
    """
    Liste toutes les équipes ou crée une nouvelle équipe.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Lister toutes les équipes.",
        responses={200: TeamSerializer(many=True)}
    )
    def get(self, request):
        teams = Team.objects.all()
        if not teams.exists():
            return Response(
                {"message": "No teams found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TeamSerializer(teams, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_description="Créer une nouvelle équipe.",
        request_body=TeamSerializer,
        responses={201: TeamSerializer, 400: "Erreur de validation"}
    )
    def post(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TeamDetail(APIView):
    """
    Récupère, modifie ou supprime une équipe spécifique.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Récupérer une équipe par son ID.",
        responses={200: TeamSerializer, 404: "Équipe non trouvée"}
    )
    def get(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        serializer = TeamSerializer(team)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Mettre à jour une équipe.",
        request_body=TeamSerializer,
        responses={200: TeamSerializer, 400: "Erreur de validation", 404: "Équipe non trouvée"}
    )
    def put(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        serializer = TeamSerializer(team, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Supprimer une équipe.",
        responses={204: "Équipe supprimée avec succès", 404: "Équipe non trouvée"}
    )
    def delete(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        team.delete()
        return Response(
            {"message": "Team deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
