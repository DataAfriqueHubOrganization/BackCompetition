from rest_framework import serializers
from .models import *


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'users', 'name', 'description', 'created_at', 'updated_at']
