from rest_framework import serializers

from back_datatour.models import Users
from allauth.account.models import EmailAddress


class UsersRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'gender',
            'country',
            'phone',
            'is_admin',
            'residence_country',
            'profession'
        ]

    # def create(self, validated_data):
    #     user = Users.objects.create_user(**validated_data)
    #     EmailAddress.objects.create(user=user, email=validated_data['email'], verified=False)
    #
    #     return user
