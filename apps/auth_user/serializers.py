from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import serializers

from .models import *


class CountrySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)

    class Meta:
        model = Country
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    residence_country = CountrySerializer(read_only=True)

    class Meta:
        model = Users
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profession', 'phone',
                'is_admin', 'country', 'residence_country','avatar' ]
      
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


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'id', 'first_name', 'last_name', 'email', 'gender', 'country', 
            'residence_country', 'profession', 'phone', 'is_verified', 'status', 'avatar'
        ]

    def create(self, validated_data):
        validated_data['is_admin'] = True
        user = Users.objects.create_user(**validated_data)
        return user
    