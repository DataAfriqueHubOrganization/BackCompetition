from rest_framework import serializers

from back_datatour.serializers import CountrySerializer
from .models import *
from apps.auth_user.serializers import UserSerializer

# class TeamSerializer(serializers.ModelSerializer):
#     country = CountrySerializer(read_only=True)
#     members = UserSerializer(many=True, read_only=True)
#     leader = UserSerializer(read_only=True)

#     class Meta:
#         model = Team
#         fields = ['name', 'country', 'members','leader',]
#     def validate(self, data):
#         """verfifer si les id des users existent envoyer un mail pour 
#         leur informer qu'on veut les ajouter et qu'il ait la possibilité d'acceter ou de refuser
#         """
#         members = data.get("members", [])
#         leader = data.get("leader", None)

#         if self.instance:
#             members = members or self.instance.members.all()

#         if len(members) > 3:
#             raise serializers.ValidationError("A team should have max 3 members")

#         if not leader:
#             raise serializers.ValidationError("A leader for the team is required")

#         if leader and leader not in members:
#             raise serializers.ValidationError("the leader need to be a team member")

#         return data
      
      
class TeamSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=Users.objects.all())
    leader = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())

    class Meta:
        model = Team
        fields = ['id', 'name', 'country', 'members', 'leader']

    def validate(self, data):
        members = data.get("members", [])
        leader = data.get("leader", None)

        if len(members) > 3:
            raise serializers.ValidationError("Une équipe peut contenir au maximum 3 membres.")
        """on a ajouter automatiquement le leader dans les membres"""
        if leader and leader not in members:
            raise serializers.ValidationError("Le leader doit aussi faire partie des membres de l’équipe.")

        return data


class TeamJoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamJoinRequest
        fields = ['id', 'user', 'team', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'team', 'created_at']
