from rest_framework import serializers
from .models import *
from apps.competition.models import CompetitionParticipant
from utils import send_emails
from rest_framework.response import Response
# class TeamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Team
#         fields = ['name', 'country', 'members','leader',]

#     def validate(self, data):
#         members = data.get("members", [])
#         leader = data.get("leader", None)

#         if len(members) > 3:
#             raise serializers.ValidationError("Une équipe peut contenir au maximum 3 membres.")

#         """
        
#         on a ajouter automatiquement le leader dans les membres
        
#         """

#         if leader and leader not in members:
#             raise serializers.ValidationError("Le leader doit aussi faire partie des membres de l’équipe.")

#         if leader:
#             for m in members:
#                 if m.country != leader.country:
#                     raise serializers.ValidationError("All members should be from the same country")

#         return data

# serializers.py
from utils import send_team_creation_emails

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'country', 'members', 'leader']

    def validate(self, data):
        members = data.get("members", [])
        leader = data.get("leader", None)

        if len(members) > 3:
            raise serializers.ValidationError("Une équipe peut contenir au maximum 3 membres.")

        if leader and leader not in members:
            raise serializers.ValidationError("Le leader doit aussi faire partie des membres de l’équipe.")

        if leader:
            for m in members:
                if m.country != leader.country:
                    raise serializers.ValidationError("Tous les membres doivent venir du même pays.")

        return data
    def create(self, validated_data):
        members = validated_data.pop('members', [])
        leader = validated_data.get('leader')
        competition = self.context.get('competition')  # ✅ récupéré depuis la vue

        if leader and leader not in members:
            members.append(leader)

        team = Team.objects.create(**validated_data)
        team.members.set([leader])  # seul le leader devient membre tout de suite

        # Créer le CompetitionParticipant pour le leader
        CompetitionParticipant.objects.create(
            user=leader,
            competition=competition,
            team=team
        )

        # Créer des invitations pour les autres membres
        invited = [m for m in members if m != leader]
        print(invited, "invited")
        for user in invited:
            TeamJoinRequest.objects.create(user=user, team=team)
            send_emails(
                subject="Invitation à rejoindre une équipe",
                message=f"Vous avez été invité à rejoindre l'équipe '{team.name}' pour la compétition '{competition.name}'.",
                recipient_list=[user.email]
            )

        send_team_creation_emails(team.name, members, leader)
        return team





class TeamJoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamJoinRequest
        fields = ['id', 'user', 'team', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'team', 'created_at']
