from rest_framework import serializers

from back_datatour.models import Users, Partner, Team
from allauth.account.models import EmailAddress


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = [
            'name',
            'description'
        ]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'name',
            'country',
            'members',
            'leader'
        ]

    def validate(self, data):
        members = data.get("members", [])
        leader = data.get("leader", None)

        if self.instance:
            members = members or self.instance.members.all()

        if len(members) != 3:
            raise serializers.ValidationError("A team should have exactly 3 members")

        if leader and leader not in members:
            raise serializers.ValidationError("the leader need to be a team member")

        return data


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
