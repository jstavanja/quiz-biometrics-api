from rest_framework import serializers
from quiz.models import Quiz
from .models import Course
from keystroke.serializers import KeystrokeTestTypeSerializer

class CourseSerializer(serializers.ModelSerializer):
  keystroke_test_type = KeystrokeTestTypeSerializer(read_only=True)
  
  class Meta:
    model = Course
    fields = '__all__'
    read_only_fields = ['pk']
