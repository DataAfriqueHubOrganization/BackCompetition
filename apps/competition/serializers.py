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

class CompetitionSerializer(serializers.ModelSerializer):
    partners = PartnerSerializer(many=True, read_only=True)
    phases = CompetitionPhaseSerializer(many=True, read_only=True, source='competitionphase_set')
    
    class Meta:
        model = Competition
        fields = ['id', 'name', 'description', 'status', 'inscription_start', 
                  'inscription_end', 'partners', 'phases']

class ChallengeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    competition_phase = serializers.SlugRelatedField(queryset=CompetitionPhase.objects.all(), slug_field='name')
    dataset_urls = serializers.SlugRelatedField(many=True, queryset=Dataset.objects.all(), slug_field='name')
    
    class Meta:
        model = Challenge
        fields = '__all__'

