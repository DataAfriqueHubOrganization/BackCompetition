from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status, permissions, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


###################################################################################
##                               REGISTER                                         #
###################################################################################


User = get_user_model()

############## REGISTER
class RegisterView(APIView):
    permission_classes = [AllowAny]  
    #  parser_classes = (MultiPartParser, FormParser)  # Gérer les fichiers uploadés
    def post(self, request):
        # serializer = RegisterSerializer(data=request.data, files=request.FILES)  # Inclure les fichiers
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Inscription réussie, vérifiez votre email."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



###################################################################################
##                                PARTNER                                        #
###################################################################################
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

###################################################################################
##                                TEAM                                       #
###################################################################################
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

############## EMAIL VERIFY
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]  
    def get(self, request, token):
        user = get_object_or_404(Users, verification_token=token)
        user.is_verified = True
        user.verification_token = None
        user.save()
        return Response({"message": "Email vérifié avec succès !"}, status=status.HTTP_200_OK)


###################################################################################
##                               LOGIN                                            #
###################################################################################

############## LOGIN
       
class LoginView(APIView):
    permission_classes = [AllowAny]     
    def post(self, request):
        # Récupérer les informations d'identification envoyées dans la requête
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Vérification si les champs sont présents
        if not username or not password:
            return Response({"error": "Nom d'utilisateur et mot de passe requis"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Authentifier l'utilisateur en passant la requête
        User = get_user_model()
        user = User.objects.filter(username=username).first()
        
        # Si l'utilisateur n'existe pas
        if not user:
            return Response({"error": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Vérifier si le compte est vérifié
        if not user.is_verified:
            return Response({"error": "Merci de vérifier votre compte"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Authentifier l'utilisateur avec les identifiants
        if not user.check_password(password):
            return Response({"error": "Mot de passe incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
          # Vérifier si le compte est vérifié
        if  user.status is False:
            return Response({"error": "Votre compte est désactivé. Veuillez contacter le support."}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        # Retourner la réponse avec les tokens et les informations de l'utilisateur
        return Response({
            'access_token': access_token,
            'refresh_token': str(refresh),
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_200_OK)
        
###################################################################################
##                               FORGOT PASSWORD                                  #
###################################################################################

############## FORGOT PASSWORD
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]  # Permet l'accès à tout le monde (même utilisateurs non authentifiés)
    def post(self, request):
        email = request.data.get('email')
        # Vérifier si l'email est valide
        if not email:
            return Response({"error": "L'email est requis."}, status=status.HTTP_400_BAD_REQUEST)
        # Utiliser le modèle personnalisé User
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Aucun utilisateur trouvé avec cet email."}, status=status.HTTP_400_BAD_REQUEST)
        # Générer le token pour réinitialiser le mot de passe
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(str(user.pk).encode())
        # Créer un lien de réinitialisation
        reset_link = f"http://{get_current_site(request).domain}/back_datatour/reset-password/{uid}/{token}/"
        print(reset_link)
        # Envoi de l'e-mail avec un message texte
        subject = 'Réinitialisation de votre mot de passe'
        message = f"Bonjour {user.username},\n\n" \
                  f"Vous avez demandé à réinitialiser votre mot de passe. Cliquez sur le lien ci-dessous pour le faire :\n\n" \
                  f"{reset_link}\n\n" \
                  f"Si vous n'avez pas demandé cette réinitialisation, ignorez cet e-mail.\n\n" \
                  f"Cordialement,\nL'équipe"

        send_mail(subject, message, 'from@example.com', [email])

        return Response({"message": "Un lien de réinitialisation de mot de passe a été envoyé à votre email."}, status=status.HTTP_200_OK)

############## RESET PASSWORD
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, uidb64, token):
        # Décoder l'UID et vérifier le token
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            User = get_user_model()  # Utiliser le modèle personnalisé
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Lien invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Token invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

        # Obtenir le new pw
        new_password = request.data.get('password')
        if not new_password:
            return Response({"error": "Le mot de passe est requis."}, status=status.HTTP_400_BAD_REQUEST)

        # Valider le pw
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Mettre à jour pw
        user.set_password(new_password)
        user.save()

        return Response({"message": "Mot de passe réinitialisé avec succès."}, status=status.HTTP_200_OK)
     
     
###################################################################################
##                               CHANGE PASSWORD                                  #
###################################################################################     

# ############## CHANGE PASSWORD

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
     
        user = request.user  # user authentifié
        
        # Récupérer les anciens et nouveaux mots de passe
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        
        # Vérifier si les champs sont fournis
        if not old_password or not new_password:
            return Response(
                {"error": "Les deux champs (ancien mot de passe et nouveau mot de passe) sont requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.check_password(old_password):
            return Response(
                {"error": "L'ancien mot de passe est incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({"error": list(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Mettre à jour le mot de passe
        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Mot de passe changé avec succès."},
            status=status.HTTP_200_OK,
        )

class DeactivateAccountView(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request, *args, **kwargs):
        # Tentative d'authentification manuelle avec JWT
        try:
            user, _ = JWTAuthentication().authenticate(request)
            if user is None or user.is_anonymous:
                return Response({"error": "Utilisateur non authentifié"}, status=status.HTTP_401_UNAUTHORIZED)
            print(f"Utilisateur authentifié: {user}")
        except Exception as e:
            return Response({"error": "Utilisateur non authentifié"}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = request.data.get('user_id', None)
        if user_id and user_id != user.id:
            if not user.is_admin:
                return Response({"error": "Permission refusée. Seuls les administrateurs peuvent désactiver d'autres comptes."}, status=status.HTTP_403_FORBIDDEN)
            try:
                user_to_deactivate = Users.objects.get(id=user_id)
            except Users.DoesNotExist:
                return Response({"error": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        else:
            user_to_deactivate = user

        if not user_to_deactivate.status:
            return Response({"message": "Le compte est déjà désactivé."}, status=status.HTTP_200_OK)

        user_to_deactivate.status = False
        user_to_deactivate.save()

        # Envoyer un email de notification
        send_mail(
            subject="Votre compte a été désactivé",
            message="Votre compte a été désactivé. Si vous pensez qu'il s'agit d'une erreur, veuillez contacter le support.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_to_deactivate.email],
            fail_silently=False,
        )
        return Response({"message": "Compte désactivé avec succès."}, status=status.HTTP_200_OK)
      
class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

class CompetitionPhaseViewSet(viewsets.ModelViewSet):
    queryset = CompetitionPhase.objects.all()
    serializer_class = CompetitionPhaseSerializer
