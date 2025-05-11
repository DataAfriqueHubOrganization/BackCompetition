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
from apps.competition.models import Competition
from django.core.mail import send_mail
from django.conf import settings

class ListOrCreateTeam(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]
    def get(self, request, country_name: str = '__all__'):
        if country_name != '__all__':
            teams = Team.objects.filter(country__name__iexact=country_name)
        else:
            teams = Team.objects.all()

        if not teams.exists():
            return Response({"message": "No teams found."}, status=status.HTTP_200_OK)

        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def get(self, request, country_name: str = '__all__'):
    #     teams = Team.objects.all()
    #     if not teams.exists():
    #         return Response(
    #             {"message": "No teams found."},
    #             status=status.HTTP_200_OK
    #         )

    #     if country_name == '__all__':
    #         serializer = TeamSerializer(teams, many=True)
    #         return Response(
    #             serializer.data,
    #             status=status.HTTP_200_OK
    #         )

    #     serializer = TeamSerializer(teams.filter(country=country_name), many=True)

    #     return Response(
    #         serializer.data,
    #         status=status.HTTP_200_OK
    #     )

    # def post(self, request):
    #     serializer = TeamSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             {
    #                 "message": "Team created",
    #                 "name": serializer.validated_data['name']
    #             },
    #             status=status.HTTP_201_CREATED
    #         )
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        competition_id = request.data.get("competition_id")
        if not competition_id:
            return Response({"detail": "competition_id manquant"}, status=400)

        competition = get_object_or_404(Competition, id=competition_id)

        serializer = TeamSerializer(data=request.data, context={"competition": competition})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Team created"}, status=201)
        return Response(serializer.errors, status=400)

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

# class UpdateTeamRequestStatus(APIView):
#     # permission_classes = [IsAuthenticated]
#     def put(self, request, pk):
#         request_join = get_object_or_404(TeamJoinRequest, pk=pk)
#         team = request_join.team

#         # Seul le leader de l'équipe peut traiter la demande
#         if request.user != team.leader:
#             return Response(
#                 {"detail": "Vous n'êtes pas autorisé à traiter cette demande."},
#                 status=status.HTTP_403_FORBIDDEN
#             )

#         status_value = request.data.get("status")  # doit être 'accepted' ou 'rejected'
#         if status_value not in ["accepted", "rejected"]:
#             return Response(
#                 {"detail": "Statut invalide. Utilisez 'accepted' ou 'rejected'."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Si accepté, vérifier que l'équipe n'est pas pleine
#         if status_value == "accepted":
#             if team.members.count() >= 3:
#                 return Response(
#                     {"detail": "Impossible d'accepter : l'équipe est déjà complète."},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             team.members.add(request_join.user)
#             competitions = CompetitionParticipant.objects.filter(team=team).values_list('competition', flat=True)
#             for competition_id in competitions:
#                 if not CompetitionParticipant.objects.filter(user=request_join.user, competition_id=competition_id).exists():
#                     CompetitionParticipant.objects.create(
#                         user=request_join.user,
#                         competition_id=competition_id,
#                         team=team
#                     )
#         request_join.status = status_value
#         request_join.save()

#         return Response(
#             {"detail": f"Demande marquée comme '{status_value}' avec succès."},
#             status=status.HTTP_200_OK
#         )
# class UpdateTeamRequestStatus(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request, pk):
#         request_join = get_object_or_404(TeamJoinRequest, pk=pk)

#         if request.user != request_join.user:
#             return Response(
#                 {"detail": "Vous n'êtes pas autorisé à répondre à cette invitation."},
#                 status=status.HTTP_403_FORBIDDEN
#             )

#         status_value = request.data.get("status")
#         if status_value not in ["accepted", "rejected"]:
#             return Response(
#                 {"detail": "Statut invalide. Utilisez 'accepted' ou 'rejected'."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         team = request_join.team

#         if status_value == "accepted":
#             if team.members.count() >= 3:
#                 return Response(
#                     {"detail": "Impossible d'accepter : l'équipe est déjà complète."},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             team.members.add(request_join.user)
#  ######
#             competitions = CompetitionParticipant.objects.filter(team=team).values_list('competition_id', flat=True)
#             for competition_id in competitions:
#                 CompetitionParticipant.objects.get_or_create(
#                     user=request_join.user,
#                     competition_id=competition_id,
#                     team=team
#                 )

#         request_join.status = status_value
#         request_join.save()

#         # Envoi d'email au leader
#         #voir si  c'est le leader qui doit 
       
#         send_mail(
#             subject=f"Réponse à l'invitation d'équipe {team.name}",
#             message=(
#                 f"L'utilisateur {request.user.get_full_name() or request.user.username} a "
#                 f"{'accepté' if status_value == 'accepted' else 'rejeté'} votre invitation à rejoindre l'équipe « {team.name} »."
#             ),
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[team.leader.email],
#             fail_silently=False
#         )

#         return Response(
#             {"detail": f"Invitation '{status_value}' avec succès."},
#             status=status.HTTP_200_OK
#         )

class UpdateTeamRequestStatus(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        request_join = get_object_or_404(TeamJoinRequest, pk=pk)
        team = request_join.team

        # Vérifier que le validateur est membre de l'équipe
        if request.user not in team.members.all():
            return Response(
                {"detail": "Seuls les membres de l’équipe peuvent valider ou rejeter une demande."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Interdire au demandeur de valider sa propre demande
        if request.user == request_join.user:
            return Response(
                {"detail": "Vous ne pouvez pas valider votre propre demande."},
                status=status.HTTP_403_FORBIDDEN
            )

        status_value = request.data.get("status")
        if status_value not in ["accepted", "rejected"]:
            return Response(
                {"detail": "Statut invalide. Utilisez 'accepted' ou 'rejected'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if status_value == "accepted":
            if team.members.count() >= 3:
                return Response(
                    {"detail": "Impossible d'accepter : l'équipe est déjà complète."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Ajouter le membre à l'équipe
            team.members.add(request_join.user)

            # L'ajouter aux compétitions de l'équipe
            competitions = CompetitionParticipant.objects.filter(team=team).values_list('competition_id', flat=True)
            for competition_id in competitions:
                CompetitionParticipant.objects.get_or_create(
                    user=request_join.user,
                    competition_id=competition_id,
                    team=team
                )

        request_join.status = status_value
        request_join.save()

        # Notifier le demandeur
        send_mail(
            subject=f"Votre demande d'intégration à l'équipe {team.name}",
            message=(
                f"Votre demande a été {'acceptée' if status_value == 'accepted' else 'rejetée'} "
                f"par {request.user.get_full_name() or request.user.username}."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request_join.user.email],
            fail_silently=False
        )

        return Response(
            {"detail": f"Demande '{status_value}' traitée avec succès."},
            status=status.HTTP_200_OK
        )

class TeamJoinRequestDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        requests = TeamJoinRequest.objects.filter(user=user)
        serializer = TeamJoinRequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, pk):
        request_join = get_object_or_404(TeamJoinRequest, pk=pk)
        serializer = TeamJoinRequestSerializer(request_join)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        request_join = get_object_or_404(TeamJoinRequest, pk=pk)
        request_join.delete()
        return Response(
            {"message": "Demande de rejoindre l'équipe supprimée."},
            status=status.HTTP_204_NO_CONTENT
        )
    # def post(self, request):
    #     user = request.user
    #     team_id = request.data.get("team_id")
    #     if not team_id:
    #         return Response({"detail": "team_id manquant"}, status=400)

    #     team = get_object_or_404(Team, id=team_id)

    #     # Vérifier si l'utilisateur a déjà envoyé une demande pour cette équipe
    #     if TeamJoinRequest.objects.filter(user=user, team=team).exists():
    #         return Response({"detail": "Vous avez déjà envoyé une demande pour cette équipe."}, status=400)

    #     # Créer la demande
    #     request_join = TeamJoinRequest.objects.create(user=user, team=team)
    #     send_mail(
    #         subject=f"Nouvelle demande d'intégration à l'équipe {team.name}",
    #         message=f"L'utilisateur {user.get_full_name() or user.username} a demandé à rejoindre votre équipe.",
    #         from_email=settings.DEFAULT_FROM_EMAIL,
    #         recipient_list=[team.leader.email],
    #         fail_silently=False
    #     )

        # return Response({"message": "Demande envoyée avec succès."}, status=201)