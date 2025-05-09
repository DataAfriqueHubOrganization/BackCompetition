from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from drf_yasg.utils import swagger_auto_schema
from .models import Challenge, Competition, CompetitionPhase,CompetitionParticipant, Team
from .serializers import *
from apps.auth_user.permissions import IsAdminUser
from utils import send_emails
from apps.team.models import TeamJoinRequest


###################################################################################
#                                   COMPETITION                                   #
###################################################################################

class CompetitionListCreate(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]

    def get(self, request):
        competitions = Competition.objects.all()
        serializer = CompetitionSerializer(competitions, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = CompetitionSerializer(data=request.data)
        if serializer.is_valid():
            competition = serializer.save()
            return Response(CompetitionSerializer(competition).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompetitionDetail(APIView):
    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]

    def get_object(self, pk):
        return get_object_or_404(Competition, pk=pk)

    def get(self, request, pk):
        competition = self.get_object(pk)
        serializer = CompetitionSerializer(competition)
        return Response(serializer.data)

    def put(self, request, pk):
        competition = self.get_object(pk)
        serializer = CompetitionSerializer(competition, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        competition = self.get_object(pk)
        competition.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


###################################################################################
#                             COMPETITIONS PHASES                                 #
###################################################################################

class CompetitionPhaseListCreate(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]

    def get(self, request):
        phases = CompetitionPhase.objects.all()
        serializer = CompetitionPhaseSerializer(phases, many=True)
        return Response(serializer.data)

    def post(self, request):
        competition_id = request.data.get('competition')
        if not competition_id:
            return Response({'detail': 'Competition ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        competition = get_object_or_404(Competition, id=competition_id)
        if competition.competitionphase_set.count() >= 2:
            return Response(
                {'detail': 'Une compétition ne peut pas avoir plus de 2 phases.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CompetitionPhaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompetitionPhaseDetail(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]

    def get_object(self, pk):
        return get_object_or_404(CompetitionPhase, pk=pk)

    def get(self, request, pk):
        phase = self.get_object(pk)
        serializer = CompetitionPhaseSerializer(phase)
        return Response(serializer.data)

    def put(self, request, pk):
        phase = self.get_object(pk)
        serializer = CompetitionPhaseSerializer(phase, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        phase = self.get_object(pk)
        phase.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

###################################################################################
#                                   CHALLENGE                                     #
###################################################################################

class ChallengeListCreate(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]

    def get(self, request):
        challenges = Challenge.objects.all()
        serializer = ChallengeSerializer(challenges, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChallengeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChallengeDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get_permissions(self):
        if self.request.method == 'put' or self.request.method == 'delete':
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]
    def get_object(self, pk):
        return get_object_or_404(Challenge, pk=pk)

    def get(self, request, pk):
        challenge = self.get_object(pk)
        serializer = ChallengeSerializer(challenge)
        return Response(serializer.data)

    def put(self, request, pk):
        challenge = self.get_object(pk)
        serializer = ChallengeSerializer(challenge, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        challenge = self.get_object(pk)
        challenge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.utils.timezone import now

class ParticipateInCompetition(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, competition_id):
        user = request.user
        competition = get_object_or_404(Competition, id=competition_id)

        # Vérifie la période d'inscription
        if competition.inscription_start > now() or competition.inscription_end < now():
            return Response(
                {"detail": "L'inscription est fermée ou pas encore ouverte."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifie si déjà inscrit
        if CompetitionParticipant.objects.filter(user=user, competition=competition).exists():
            return Response(
                {"detail": "Vous êtes déjà inscrit à cette compétition."},
                status=status.HTTP_200_OK
            )

        team_id = request.data.get("team_id")
        print(team_id, "tttttt")
        if team_id:
            #  Rejoindre une équipe existante
            team = get_object_or_404(Team, id=team_id)

            if team.members.filter(id=user.id).exists():
                return Response({"detail": "Vous êtes déjà membre de cette équipe."}, status=status.HTTP_400_BAD_REQUEST)

            if team.members.count() >= 3:
                return Response({"detail": "Cette équipe est déjà complète."}, status=status.HTTP_400_BAD_REQUEST)

            # Créer la demande
            TeamJoinRequest.objects.create(user=user, team=team)

            # Notification au leader
            send_emails(
                subject="Demande d'intégration à l'équipe",
                message=f"{user.username} souhaite rejoindre votre équipe '{team.name}' pour la compétition '{competition.name}'.",
                recipient_list=[team.leader.email]
            )

            # Crée l'entrée dans CompetitionParticipant avec la team liée (en attente de validation)
            CompetitionParticipant.objects.create(user=user, competition=competition, team=team)

            return Response(
                {"detail": "Demande envoyée au leader de l'équipe."},
                status=status.HTTP_201_CREATED
            )

        #  Aucun team_id fourni et création de team non gérée ici
        return Response(
            {"detail": "Veuillez rejoindre une équipe existante ou créer une équipe via l'API dédiée."},
            status=status.HTTP_400_BAD_REQUEST
        )
