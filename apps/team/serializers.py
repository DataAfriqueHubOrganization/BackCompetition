from rest_framework import serializers

from .models import *


class TeamSerializer(serializers.ModelSerializer):
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

        if leader:
            for m in members:
                if m.country != leader.country:
                    raise serializers.ValidationError("All members should be from the same country")

        return data
      
