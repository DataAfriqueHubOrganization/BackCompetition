from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Users,Country
from .serializers import RegisterSerializer, UserSerializer,CountrySerializer
from .permissions import IsAdminOrReadOnly
from rest_framework import viewsets
User = get_user_model()

##########################################
#            REGISTER & VERIFY EMAIL     #
##########################################

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Inscription réussie, vérifiez votre email."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        user = get_object_or_404(Users, verification_token=token)
        user.is_verified = True
        user.verification_token = None
        user.save()
        return Response({"message": "Email vérifié avec succès !"}, status=status.HTTP_200_OK)

##########################################
#                 LOGIN                  #
##########################################

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Nom d'utilisateur et mot de passe requis"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            return Response({"error": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_verified:
            return Response({"error": "Merci de vérifier votre compte"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.status:
            return Response({"error": "Votre compte est désactivé. Veuillez contacter le support."}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)

        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, status=status.HTTP_200_OK)

##########################################
#         FORGOT & RESET PASSWORD        #
##########################################

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "L'email est requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Aucun utilisateur trouvé avec cet email."}, status=status.HTTP_400_BAD_REQUEST)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(str(user.pk).encode())
        reset_link = f"http://{get_current_site(request).domain}/auth/reset-password/{uid}/{token}/"
        print(reset_link)

        subject = 'Réinitialisation de votre mot de passe'
        message = f"Bonjour {user.username},\n\n" \
                  f"Cliquez sur le lien ci-dessous pour réinitialiser votre mot de passe :\n{reset_link}\n\n" \
                  f"Si vous n'avez pas fait cette demande, ignorez cet email."

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        return Response({"message": "Un lien de réinitialisation de mot de passe a été envoyé à votre email."}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"error": "Lien invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Token invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('password')
        if not new_password:
            return Response({"error": "Le mot de passe est requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({"error": list(e)}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Mot de passe réinitialisé avec succès."}, status=status.HTTP_200_OK)

##########################################
#           CHANGE PASSWORD              #
##########################################

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response({"error": "Ancien et nouveau mot de passe requis."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({"error": "L'ancien mot de passe est incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({"error": list(e)}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Mot de passe changé avec succès."}, status=status.HTTP_200_OK)

##########################################
#        DEACTIVATE ACCOUNT              #
##########################################

class DeactivateAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user, _ = JWTAuthentication().authenticate(request)
            if not user or user.is_anonymous:
                raise Exception
        except Exception:
            return Response({"error": "Utilisateur non authentifié"}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = request.data.get('user_id')
        user_to_deactivate = user

        if user_id and user_id != user.id:
            if not user.is_admin:
                return Response({"error": "Action non autorisée."}, status=status.HTTP_403_FORBIDDEN)
            user_to_deactivate = get_object_or_404(Users, id=user_id)

        if not user_to_deactivate.status:
            return Response({"message": "Le compte est déjà désactivé."}, status=status.HTTP_200_OK)

        user_to_deactivate.status = False
        user_to_deactivate.save()

        send_mail(
            "Votre compte a été désactivé",
            "Si vous pensez qu'il s'agit d'une erreur, contactez le support.",
            settings.DEFAULT_FROM_EMAIL,
            [user_to_deactivate.email],
        )

        return Response({"message": "Compte désactivé avec succès."}, status=status.HTTP_200_OK)

##########################################
#            USER CRUD                   #
##########################################

class ListUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = Users.objects.all()
        if not users.exists():
            return Response({"message": "Aucun utilisateur trouvé."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(Users, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = get_object_or_404(Users, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(Users, pk=pk)
        user.delete()
        return Response({"message": "Utilisateur supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)

# country api
# views.py

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

#Admin API
from rest_framework import viewsets, permissions
from .serializers import AdminUserSerializer

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.filter(is_admin=True)
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ajuste selon les besoins

    def perform_create(self, serializer):
        serializer.save(is_admin=True)
