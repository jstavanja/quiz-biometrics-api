from rest_framework import serializers
from .models import Quiz

from keystroke.serializers import KeystrokeTestTypeSerializer

class QuizSerializer(serializers.ModelSerializer):
  keystroke_test_type = KeystrokeTestTypeSerializer(read_only=True)
  
  class Meta:
    model = Quiz
    fields = '__all__'
    read_only_fields = ['pk']
