from rest_framework import serializers
from .models import *


class AnnouncementSerializer(serializers.ModelSerializer):
    # Display the user's string representation (e.g., username) in responses.
    # read_only=True ensures it cannot be set via API input.
    user = serializers.StringRelatedField(read_only=True)
    # Alternative: If you want to show the user's ID instead:
    # user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Announcement
        # Exclude 'user' from direct input, include it for output
        fields = ['id', 'user', 'name', 'description', 'created_at', 'updated_at']
        # Explicitly mark fields that are set automatically or read-only
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']