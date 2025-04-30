from rest_framework import serializers
from .models import *


class DatasetSerializer(serializers.ModelSerializer):
    dataset_train = serializers.FileField(required=True)
    dataset_test = serializers.FileField(required=False)
    dataset_submission = serializers.FileField(required=True)
    description = serializers.CharField(required=True)

    class Meta:
        model = Dataset
        fields = '__all__'
