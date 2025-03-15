from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status
from rest_framework import generics
from .models import Comment, Announcement
from .serializers import CommentSerializer, AnnouncementSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission, SAFE_METHODS

from back_datatour.serializers import UsersRegisterSerializer


# Create your views here.
class UserRegister(APIView):
    def post(self, request):
        user = UsersRegisterSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response({'message': 'utilisateur enregistre avec success'}, status=status.HTTP_200_OK)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)


class IsOwnerOrAdmin(BasePermission):
    """
    Autorise la modification ou la suppression seulement si l'utilisateur est
    le propriétaire (champ 'users') ou un administrateur.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.users == request.user or request.user.is_staff or request.user.is_superuser



# Pour le modèle Comment
class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

# Pour le modèle Announcement
class AnnouncementListCreateAPIView(generics.ListCreateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

class AnnouncementRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]