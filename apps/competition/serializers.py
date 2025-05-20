from rest_framework import serializers
# from back_datatour.models import Partner, Team, Users
from apps.partner.models import  Partner
from apps.partner.serializers import PartnerSerializer
from django.core.mail import send_mail
from django.conf import settings
from .models import *

class CompetitionPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionPhase
        fields = ['id', 'competition', 'name', 'start_date', 'end_date']


# class CompetitionCreateSerializer(serializers.ModelSerializer):
#     partners = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=False)
#     # phases = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=False)

#     class Meta:
#         model = Competition
#         fields = ['name', 'description', 'status', 'inscription_start', 'inscription_end', 'partners', 'phases']

#     def create(self, validated_data):
#         partners_data = validated_data.pop('partners', [])
#         phases_data = validated_data.pop('phases', [])

#         competition = Competition.objects.create(**validated_data)

#         # Set ManyToMany partners
#         if partners_data:
#             competition.partners.set(partners_data)

#         # Set ForeignKeys on CompetitionPhase objects
#         from apps.competition.models import CompetitionPhase
#         CompetitionPhase.objects.filter(id__in=phases_data).update(competition=competition)

#         return competition

# class CompetitionSerializer(serializers.ModelSerializer):
#     partners = serializers.PrimaryKeyRelatedField(queryset=Partner.objects.all(), many=True)
    
#     class Meta:
#         model = Competition
#         fields = ['id', 'name', 'description', 'status', 'inscription_start', 'inscription_end', 'partners']

class CompetitionSerializer(serializers.ModelSerializer):
    partners = serializers.PrimaryKeyRelatedField(queryset=Partner.objects.all(), many=True)
    phases = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = ['id', 'competition_image','name', 'description', 'status', 'inscription_start', 'inscription_end', 'partners', 'phases']

    def get_phases(self, obj):
        phases = CompetitionPhase.objects.filter(competition=obj)
        return [phase.id for phase in phases]

class ChallengeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    competition_phase = serializers.SlugRelatedField(queryset=CompetitionPhase.objects.all(), slug_field='name')
    dataset_urls = serializers.SlugRelatedField(many=True, queryset=Dataset.objects.all(), slug_field='name')
    
    class Meta:
        model = Challenge
        fields = '__all__'



class CompetitionParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionParticipant
        fields = ['id', 'user', 'competition', 'team', 'joined_at']
        read_only_fields = ['id', 'user', 'joined_at']
