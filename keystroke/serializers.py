from rest_framework import serializers
from .models import KeystrokeTestType, KeystrokeTestSession


class KeystrokeTestTypeSerializer(serializers.ModelSerializer):

  class Meta:
    model = KeystrokeTestType
    fields = '__all__'
    read_only_fields = ['pk']


class KeystrokeTestSessionSerializer(serializers.ModelSerializer):

  class Meta:
    model = KeystrokeTestSession
    fields = '__all__'
    read_only_fields = ['pk']

