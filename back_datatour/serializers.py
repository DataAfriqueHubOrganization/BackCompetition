from allauth.account.models import EmailAddress
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from back_datatour.models import Partner, Team, Users
from back_datatour.models import Users, Partner, Team
from allauth.account.models import EmailAddress
from django.core.mail import send_mail
from django.conf import settings
from .models import *

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'name', 'description', 'logo', 'website_url'  ]

class CountrySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    
    class Meta:
        model = Country
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    residence_country = CountrySerializer(read_only=True)

    class Meta:
        model = Users
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profession', 'phone',
                'is_admin', 'country', 'residence_country' ]

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
      

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["first_name", "last_name","username", "email", "password", "gender", "country", "residence_country", "profession", "phone"]
        # fields = ["username", "email", "password", "gender", "country", "residence_country", "profession", "phone", "logo"]

    def validate_email(self, value):
        """ Vérifier que l'email est unique """
        if Users.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

    def create(self, validated_data):
        # Récupérer et supprimer le mot de passe avant d'instancier l'objet
        password = validated_data.pop("password")  

        # Créer l'utilisateur sans mot de passe
        user = Users(**validated_data)
        user.is_verified = False
        user.generate_verification_token()

        # Hasher le mot de passe avant d'enregistrer
        user.set_password(password)  

        # Sauvegarder l'utilisateur
        user.save()

        # Envoyer l'email de vérification (optionnel)
        verification_link = f"http://127.0.0.1:8000/back_datatour/auth/verify-email/{user.verification_token}/"
        print(verification_link)
        send_mail(
            subject="Vérification de votre compte",
            message=f"Cliquez sur ce lien pour vérifier votre compte : {verification_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return user


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

class DatasetSerializer(serializers.ModelSerializer):
    dataset_train = serializers.FileField(required=True)
    dataset_test = serializers.FileField(required=False)
    dataset_submission = serializers.FileField(required=True)
    description = serializers.CharField(required=True)

    class Meta:
        model = Dataset
        fields = '__all__'

class ChallengeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    competition_phase = serializers.SlugRelatedField(queryset=CompetitionPhase.objects.all(), slug_field='name')
    dataset_urls = serializers.SlugRelatedField(many=True, queryset=Dataset.objects.all(), slug_field='name')
    
    class Meta:
        model = Challenge
        fields = '__all__'



class SubmissionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    team = serializers.SlugRelatedField(queryset=Team.objects.all(), slug_field='name')
    challenge = serializers.SlugRelatedField(queryset=Challenge.objects.all(), slug_field='name')
    file = serializers.FileField()  

    class Meta:
        model = Submission
        fields = '__all__'

class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    team = serializers.SlugRelatedField(queryset=Team.objects.all(), slug_field='name')
    competition_phase = serializers.SlugRelatedField(queryset=CompetitionPhase.objects.all(), slug_field='name')
    
    class Meta:
        model = Leaderboard
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'users', 'competition_phase', 'content', 'created_at', 'updated_at']

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'users', 'name', 'description', 'created_at', 'updated_at']
