from rest_framework import serializers
from .models import *


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'name', 'description', 'logo', 'website_url'  ]
