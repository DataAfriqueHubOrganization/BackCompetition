from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from back_datatour.models import Partner, Team
from back_datatour.serializers import UsersRegisterSerializer, PartnerSerializer, TeamSerializer


# Create your views here.
class UserRegister(APIView):
    def post(self, request):
        user = UsersRegisterSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response({'message': 'utilisateur enregistre avec success'}, status=status.HTTP_200_OK)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)


class ListOrCreatePartner(APIView):
    def get(self, request):
        partners = Partner.objects.all()
        if not partners.exists():
            return Response(
                {"message": "No partners found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PartnerSerializer(partners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        partner = PartnerSerializer(data=request.data)
        if partner.is_valid():
            partner.save()
            return Response(
                partner.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            partner.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class PartnerDetail(APIView):
    def get(self, request, pk):
        partner = get_object_or_404(Partner, pk=pk)
        serializer = PartnerSerializer(partner)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):
        partner = get_object_or_404(Partner, pk=pk)
        serializer = PartnerSerializer(
            partner,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        partner = get_object_or_404(Partner, pk=pk)
        partner.delete()
        return Response(
            {"message": "Partner deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class ListOrCreateTeam(APIView):
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
    def get(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        serializer = TeamSerializer(team)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        serializer = TeamSerializer(team, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        team.delete()
        return Response({"message": "Team deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
