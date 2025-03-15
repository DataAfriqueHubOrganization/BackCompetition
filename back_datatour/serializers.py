from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Country, Team, Partner, Competition, CompetitionPhase,
    Leaderboard, Dataset, Challenge, Submission, Comment, Announcement
)

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

class CountrySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    
    class Meta:
        model = Country
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    country = serializers.SlugRelatedField(queryset=Country.objects.all(), slug_field='name', required=False, allow_null=True)
    residence_country = serializers.SlugRelatedField(queryset=Country.objects.all(), slug_field='name', required=False, allow_null=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password', 'gender', 'country',
                 'residence_country', 'profession', 'phone', 'is_admin', 'first_name', 'last_name')
        read_only_fields = ('id', 'updated_at')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'profession': {'required': False, 'allow_null': True},
            'phone': {'required': False, 'allow_null': True},
            'gender': {'required': False, 'allow_null': True},
        }
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Add any additional user representation if needed
        return ret

class TeamSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    country = serializers.SlugRelatedField(queryset=Country.objects.all(), slug_field='name')
    members = serializers.SlugRelatedField(many=True, queryset=Users.objects.all(), slug_field='username')
    leader = serializers.SlugRelatedField(queryset=Users.objects.all(), slug_field='username', required=False, allow_null=True)
    
    class Meta:
        model = Team
        fields = ('id', 'name', 'country', 'members', 'leader', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Enhance the representation with full user details if needed
        if 'members' in ret:
            members_data = []
            for member in instance.members.all():
                members_data.append({
                    'id': str(member.id),
                    'username': member.username,
                    'email': member.email,
                    'full_name': f"{member.first_name} {member.last_name}".strip()
                })
            ret['members'] = members_data
        if instance.leader:
            ret['leader'] = {
                'id': str(instance.leader.id),
                'username': instance.leader.username,
                'email': instance.leader.email,
                'full_name': f"{instance.leader.first_name} {instance.leader.last_name}".strip()
            }
        return ret

class PartnerSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    
    class Meta:
        model = Partner
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class CompetitionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    
    class Meta:
        model = Competition
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class CompetitionPhaseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    competition = serializers.SlugRelatedField(queryset=Competition.objects.all(), slug_field='name')
    
    class Meta:
        model = CompetitionPhase
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    team = serializers.SlugRelatedField(queryset=Team.objects.all(), slug_field='name')
    competition_phase = serializers.SlugRelatedField(queryset=CompetitionPhase.objects.all(), slug_field='name')
    
    class Meta:
        model = Leaderboard
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class DatasetSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    
    class Meta:
        model = Dataset
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class ChallengeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    competition_phase = serializers.SlugRelatedField(queryset=CompetitionPhase.objects.all(), slug_field='name')
    dataset_urls = serializers.SlugRelatedField(many=True, queryset=Dataset.objects.all(), slug_field='name')
    
    class Meta:
        model = Challenge
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class SubmissionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    team = serializers.SlugRelatedField(queryset=Team.objects.all(), slug_field='name')
    challenge = serializers.SlugRelatedField(queryset=Challenge.objects.all(), slug_field='name')
    
    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    users = serializers.SlugRelatedField(queryset=Users.objects.all(), slug_field='username')
    compétition_phase = serializers.SlugRelatedField(queryset=CompetitionPhase.objects.all(), slug_field='name')
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.users:
            ret['users'] = {
                'id': str(instance.users.id),
                'username': instance.users.username,
                'email': instance.users.email,
                'full_name': f"{instance.users.first_name} {instance.users.last_name}".strip()
            }
        return ret

class AnnouncementSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    users = serializers.SlugRelatedField(queryset=Users.objects.all(), slug_field='username')
    
    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.users:
            ret['users'] = {
                'id': str(instance.users.id),
                'username': instance.users.username,
                'email': instance.users.email,
                'full_name': f"{instance.users.first_name} {instance.users.last_name}".strip()
            }
        return ret
