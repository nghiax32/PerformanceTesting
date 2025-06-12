from rest_framework import serializers
from .models import TestRun

class TestRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRun
        fields = '__all__'