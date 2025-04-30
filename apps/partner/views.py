from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from .models import Partner
from .serializers import PartnerSerializer


###################################################################################
#                                 PARTNERS                                        #
###################################################################################

class ListOrCreatePartner(APIView):
    """
    Gère la liste et la création des partenaires.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Liste tous les partenaires disponibles.",
        responses={200: PartnerSerializer(many=True), 404: "Aucun partenaire trouvé"}
    )
    def get(self, request):
        partners = Partner.objects.all()
        if not partners.exists():
            return Response(
                {"message": "Aucun partenaire trouvé."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = PartnerSerializer(partners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Créer un nouveau partenaire.",
        request_body=PartnerSerializer,
        responses={201: PartnerSerializer, 400: "Erreur de validation"}
    )
    def post(self, request):
        serializer = PartnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartnerDetail(APIView):
    """
    Récupère, met à jour ou supprime un partenaire spécifique.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Récupère les détails d’un partenaire.",
        responses={200: PartnerSerializer, 404: "Partenaire non trouvé"}
    )
    def get(self, request, pk):
        partner = get_object_or_404(Partner, pk=pk)
        serializer = PartnerSerializer(partner)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Met à jour un partenaire existant.",
        request_body=PartnerSerializer,
        responses={200: PartnerSerializer, 400: "Erreur de validation", 404: "Partenaire non trouvé"}
    )
    def put(self, request, pk):
        partner = get_object_or_404(Partner, pk=pk)
        serializer = PartnerSerializer(partner, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Supprime un partenaire existant.",
        responses={204: "Supprimé avec succès", 404: "Partenaire non trouvé"}
    )
    def delete(self, request, pk):
        partner = get_object_or_404(Partner, pk=pk)
        partner.delete()
        return Response({"message": "Partenaire supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
