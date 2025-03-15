from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Competition, CompetitionPhase
from .serializers import CompetitionSerializer, CompetitionPhaseSerializer


from back_datatour.serializers import UsersRegisterSerializer


# Create your views here.
class UserRegister(APIView):
    def post(self, request):
        user = UsersRegisterSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response({'message': 'utilisateur enregistre avec success'}, status=status.HTTP_200_OK)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)


class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

class CompetitionPhaseViewSet(viewsets.ModelViewSet):
    queryset = CompetitionPhase.objects.all()
    serializer_class = CompetitionPhaseSerializer
