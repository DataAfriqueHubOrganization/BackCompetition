from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny  
from django.contrib.auth import get_user_model
from utils import send_emails  

###################################################################################
#                                   TEAM                                          #
###################################################################################



User = get_user_model()

class ListOrCreateTeam(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Lister toutes les équipes.",
        responses={200: TeamSerializer(many=True)}
    )
    def get(self, request):
        teams = Team.objects.all()
        if not teams.exists():
            return Response(
                {"message": "Aucune équipe trouvée."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Créer une nouvelle équipe.",
        request_body=TeamSerializer,
        responses={201: TeamSerializer, 400: "Erreur de validation"}
    )
    def post(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            team = serializer.save()

            # Envoyer un email à chaque membre sauf le leader
            members_ids = request.data.get("members", [])
            leader_id = request.data.get("leader")

            for member_id in members_ids:
                if member_id != leader_id:
                    try:
                        user = User.objects.get(pk=member_id)
                        send_emails(
                            subject="Invitation à rejoindre une équipe",
                            message=f"Bonjour {user.username},\n\nVous avez été invité à rejoindre l’équipe '{team.name}'. Connectez-vous pour accepter ou refuser cette invitation.",
                            recipient_list=[user.email]
                        )
                    except User.DoesNotExist:
                        pass  # Ignore si l'utilisateur n'existe pas

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

class UpdateTeamRequestStatus(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        request_join = get_object_or_404(TeamJoinRequest, pk=pk)
        team = request_join.team

        # Seul le leader de l'équipe peut traiter la demande
        if request.user != team.team_leader:
            return Response(
                {"detail": "Vous n'êtes pas autorisé à traiter cette demande."},
                status=status.HTTP_403_FORBIDDEN
            )

        status_value = request.data.get("status")  # doit être 'accepted' ou 'rejected'
        if status_value not in ["accepted", "rejected"]:
            return Response(
                {"detail": "Statut invalide. Utilisez 'accepted' ou 'rejected'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Si accepté, vérifier que l'équipe n'est pas pleine
        if status_value == "accepted":
            if team.members.count() >= 3:
                return Response(
                    {"detail": "Impossible d'accepter : l'équipe est déjà complète."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            team.members.add(request_join.user)

        request_join.status = status_value
        request_join.save()

        return Response(
            {"detail": f"Demande marquée comme '{status_value}' avec succès."},
            status=status.HTTP_200_OK
        )
