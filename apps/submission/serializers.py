from rest_framework import serializers
from .models import *
from apps.team.models import Team
from apps.competition.models import Challenge, CompetitionPhase


class SubmissionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    team = serializers.SlugRelatedField(queryset=Team.objects.all(), slug_field='name')
    challenge = serializers.SlugRelatedField(queryset=Challenge.objects.all(), slug_field='name')
    file = serializers.FileField()  

    class Meta:
        model = Submission
        fields = '__all__'

# class LeaderboardSerializer(serializers.ModelSerializer):
#     id = serializers.UUIDField(format='hex_verbose', read_only=True)
#     team = serializers.SlugRelatedField(queryset=Team.objects.all(), slug_field='name')
#     competition_phase = serializers.SlugRelatedField(queryset=CompetitionPhase.objects.all(), slug_field='name')
    
#     class Meta:
#         model = Leaderboard
#         fields = '__all__'
#         read_only_fields = ('id', 'created_at', 'updated_at')

