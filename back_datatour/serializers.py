from rest_framework import serializers
from allauth.account.models import EmailAddress
from django.core.mail import send_mail
from django.conf import settings
from .models import *

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ["username", "email", "password", "gender", "country", "residence_country", "profession", "phone"]
        # fields = ["username", "email", "password", "gender", "country", "residence_country", "profession", "phone", "logo"]

    def validate_email(self, value):
        """ Vérifier que l'email est unique """
        if Users.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

    def create(self, validated_data):
        # Récupérer et supprimer le mot de passe avant d'instancier l'objet
        password = validated_data.pop("password")  

        # Créer l'utilisateur sans mot de passe
        user = Users(**validated_data)
        user.is_verified = False
        user.generate_verification_token()

        # Hasher le mot de passe avant d'enregistrer
        user.set_password(password)  

        # Sauvegarder l'utilisateur
        user.save()

        # Envoyer l'email de vérification (optionnel)
        verification_link = f"http://127.0.0.1:8000/back_datatour/auth/verify-email/{user.verification_token}/"
        send_mail(
            subject="Vérification de votre compte",
            message=f"Cliquez sur ce lien pour vérifier votre compte : {verification_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return user
