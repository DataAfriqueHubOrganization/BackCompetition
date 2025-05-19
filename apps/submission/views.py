from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from .models import Submission 
from .serializers import SubmissionSerializer #, LeaderboardSerializer
from django.utils import timezone
from apps.competition.models import CompetitionParticipant
import os
from .evaluations import evaluate_submission

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
        
        reference_path = challenge.dataset_urls.files.filter(file_type='SOLUTION').first()
        if not reference_path:
            return Response({"error": "Fichier de référence introuvable pour ce défi."}, status=status.HTTP_400_BAD_REQUEST)
        #definir dynanmiquement metrics:
        metric = challenge.metric
        score = evaluate_submission(file_path, reference_path, metric)
        
        if score.get("status") == "error":
            return Response({"error": score.get("message")}, status=status.HTTP_400_BAD_REQUEST)
        # Sauvegarder le score dans private, puis le comparer au public score, si c'est > om modifie le public score sinon on garde
        else:
       # Créer la soumission avec le score obtenu      
            Submission.objects.create(
                team=team_user,
                challenge=challenge,
                file=file_path,
                score=score.get("score")
            )
              
    #lister les soumission d'un participant   
    def get(self, request, participant_id):
        # team_user = request.user.team
        participant = CompetitionParticipant.objects.filter(user=request.user, id=participant_id).first() 
        team_user = participant.team
        challenge = request.get("challenge")
        submission = Submission.objects.filter(team= team_user, challenge=challenge)
        if not submission:
            return Response({"error": "Aucune soumission trouvée."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubmissionSerializer(submission, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# lister dernier submission des participants
# class SubmissionListAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request, participant_id):
#         # team_user = request.user.team
#         participant = CompetitionParticipant.objects.filter(user=request.user, id=participant_id).first() 
#         team_user = participant.team
#         submission = Submission.objects.filter(team= team_user).order_by('-created_at')[:1]
#         if not submission:
#             return Response({"error": "Aucune soumission trouvée."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = SubmissionSerializer(submission, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)