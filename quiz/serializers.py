from rest_framework import serializers
from .models import Quiz

from course.serializers import CourseSerializer
from .models import Quiz

class QuizSerializer(serializers.ModelSerializer):
  course = CourseSerializer(read_only=True)
  
  class Meta:
    model = Quiz
    fields = '__all__'
    read_only_fields = ['pk']
