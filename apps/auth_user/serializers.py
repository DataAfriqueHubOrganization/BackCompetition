from allauth.account.models import EmailAddress
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from back_datatour.serializers import CountrySerializer
# from back_datatour.models import Partner, Team, Users
from django.conf import settings
from .models import *
# from django.contrib.sites.models import Site
from django.urls import reverse
from decouple import config
 


class UserSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    residence_country = CountrySerializer(read_only=True)

    class Meta:
        model = Users
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profession', 'phone',
                'is_admin', 'country', 'residence_country' ]
      

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["first_name", "last_name","username", "email", "password", "gender", "country", "residence_country", "profession", "phone"]
        # fields = ["username", "email", "password", "gender", "country", "residence_country", "profession", "phone", "logo"]

    def validate_email(self, value):
        """ Vérifier que l'email est unique """
        if Users.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Users(**validated_data)
        user.is_verified = False
        user.generate_verification_token()
        user.set_password(password)
        user.save()

        path = reverse('verify-email', kwargs={'token': user.verification_token})
        verification_link = f"{settings.DOMAIN_NAME}{path}"

        print(verification_link)

        send_mail(
            subject="Vérification de votre compte",
            message=f"Cliquez sur ce lien pour vérifier votre compte : {verification_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user
    