from rest_framework import serializers
from django.conf import settings
from .models import *



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'users', 'competition_phase', 'content', 'created_at', 'updated_at']
