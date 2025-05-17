from rest_framework import viewsets, status, permissions, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema

from .models import Submission, Leaderboard
from .serializers import SubmissionSerializer, LeaderboardSerializer
from django.utils import timezone
from apps.competition.models import CompetitionParticipant
import os
###################################################################################
#                                SUBMISSION                                       #
###################################################################################
class SubmissionCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, participant_id):
        # team_user = request.user.team
        participant = CompetitionParticipant.objects.filter(user=request.user, id=participant_id).first() 
        team_user = participant.team
        today = timezone.now()
        day_submission = Submission.objects.filter(team= team_user, created_at=today.date()).count()

        if day_submission >= Submission.limit:
            return Response({"error": "Vous avez atteint la limite de soumissions pour aujourd'hui."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not participant:
            return Response({"error": "Participant non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        uploaded_field = request.FILES.get('file')
        if not uploaded_field:
            return Response({"error": "Aucun fichier soumis."}, status=status.HTTP_400_BAD_REQUEST) 
        competition_name = participant.competition.name.replace(" ", "_").lower() 
        team_name= participant.team.name.replace(" ", "_").lower()
        challenge = request.get("challenge")
        if not challenge:
            return Response({"error": "Aucun défi trouvé."}, status=status.HTTP_400_BAD_REQUEST)
        challenge_name = challenge.name.replace(" ", "_").lower()
        phase_name = challenge_name.competition_phase.replace(" ", "_").lower()
        base_path = os.path.join("competitions", competition_name, phase_name)
        folder_path = os.path.join(base_path, team_name)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, uploaded_field.name)
        #fonction d'evaluation avec  score actualisé
        # with open(file_path, 'wb+') as destination:
        #     for chunk in uploaded_field.chunks():
        #         destination.write(chunk)
        #score = 
        # Submission.objects.create(team=team_name, challenge=challenge, file=uploaded_field, score=score)
        
        """
        on prend le fichier qu'on stock dans un dossier en le renommant
        pour chaque compétition on a un dossier
        dossier  datatour 2025> dossier phases(phase 1, phase 2)> dossier team>fichier de soumission à renommer 
        uniformément suivant les paramèrtres de la compétition
        """
        
        
        
# class SubmissionViewSet(viewsets.ModelViewSet):
#     """
#     Permet de gérer les soumissions des participants à une compétition.
#     """
#     serializer_class = SubmissionSerializer
#     permission_classes = [permissions.AllowAny]
#     parser_classes = [MultiPartParser, FormParser]

#     def get_queryset(self):
#         return Submission.objects.all()

#     @swagger_auto_schema(
#         operation_description="Uploader une soumission à une compétition.",
#         request_body=SubmissionSerializer,
#         responses={
#             201: "Soumission enregistrée avec succès.",
#             400: "Données invalides."
#         }
#     )
#     def create(self, request, *args, **kwargs):
#         return super().create(request, *args, **kwargs)


###################################################################################
#                                LEADERBOARD                                      #
###################################################################################

# class LeaderboardViewSet(viewsets.ModelViewSet):
#     """
#     Affiche et met à jour les scores des participants à une compétition.
#     """
#     queryset = Leaderboard.objects.all()
#     serializer_class = LeaderboardSerializer
#     permission_classes = [permissions.AllowAny]
