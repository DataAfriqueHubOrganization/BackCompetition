from rest_framework import serializers

from back_datatour.models import Users
from allauth.account.models import EmailAddress


from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from .models import Users

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ["username", "email", "password", "gender", "country", "residence_country", "profession", "phone"]

    def validate_email(self, value):
        """ Vérifier que l'email est unique """
        if Users.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

    def create(self, validated_data):
        # Créer l'utilisateur mais ne le sauvegarder que plus tard
        user = Users(**validated_data)
        user.is_verified = False
        user.generate_verification_token()

        # Envoyer l'email de vérification
        verification_link = f"http://127.0.0.1:8000/back_datatour/auth/verify-email/{user.verification_token}/"
        send_mail(
            "Vérification de votre compte",
            f"Bonjour {user.username}, cliquez sur le lien pour vérifier votre compte : {verification_link}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        # Sauvegarder l'utilisateur après l'envoi de l'email
        user.save()

        return user
