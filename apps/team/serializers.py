from rest_framework import serializers

from back_datatour.serializers import CountrySerializer
from .models import *
from apps.auth_user.serializers import UserSerializer

class TeamSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    leader = UserSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ['name', 'country', 'members','leader',]
    def validate(self, data):
        members = data.get("members", [])
        leader = data.get("leader", None)

        if self.instance:
            members = members or self.instance.members.all()

        if len(members) != 3:
            raise serializers.ValidationError("A team should have exactly 3 members")

        if not leader:
            raise serializers.ValidationError("A leader for the team is required")

        if leader and leader not in members:
            raise serializers.ValidationError("the leader need to be a team member")

        return data
      
