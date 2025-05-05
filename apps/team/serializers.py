from rest_framework import serializers
from .models import *

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'country', 'members','leader',]

    def validate(self, data):
        members = data.get("members", [])
        leader = data.get("leader", None)

        if len(members) > 3:
            raise serializers.ValidationError("Une équipe peut contenir au maximum 3 membres.")

        """
        
        on a ajouter automatiquement le leader dans les membres
        
        """

        if leader and leader not in members:
            raise serializers.ValidationError("Le leader doit aussi faire partie des membres de l’équipe.")

        if leader:
            for m in members:
                if m.country != leader.country:
                    raise serializers.ValidationError("All members should be from the same country")

        return data


class TeamJoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamJoinRequest
        fields = ['id', 'user', 'team', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'team', 'created_at']
