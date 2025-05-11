# serializers.py
from rest_framework import serializers
from django.conf import settings
from .models import Comment, CompetitionPhase # Import CompetitionPhase if not already
# from apps.auth_user.models import Users # Import User if needed for representation

class CommentSerializer(serializers.ModelSerializer):
    # Display user's string representation, read-only
    user = serializers.StringRelatedField(read_only=True)

    # Accept CompetitionPhase ID as input, validate it exists
    # Also displays the ID in the output
    competition_phase = serializers.PrimaryKeyRelatedField(
        queryset=CompetitionPhase.objects.all()
    )
    # Alternative: If you want to display the CompetitionPhase name instead of ID in output:
    competition_phase_details = serializers.StringRelatedField(source='competition_phase', read_only=True)
    # And add 'competition_phase_details' to fields list, keep competition_phase write_only=True or exclude from fields output.
    # Let's keep it simple for now with PrimaryKeyRelatedField.

    class Meta:
        model = Comment
        fields = '__all__'

        