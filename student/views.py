# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins
from rest_framework.response import Response

from student.models import Student
from quiz.models import Quiz
from keystroke.models import KeystrokeTestSession

from student.serializers import StudentSerializer

class StudentAPIView(generics.ListAPIView):
  lookup_field = 'pk'
  serializer_class = StudentSerializer

  def get_queryset(self):
    return Student.objects.all()

  def perform_create(self, serializer):
    serializer.save()

  def post(self, request, *args, **kwargs):
    user_id = request.POST.get('user_id')

    try:
      image = request.FILES['face_image']
    except KeyError:
      raise ParseError('Request has no resource file attached')
      
    timing_matrix = request.POST.get('timing_matrix')
    quiz_id = request.POST.get('quiz_id')

    student = Student(moodle_username = user_id, face_image = image)

    quiz = Quiz.objects.filter(id=quiz_id)[0]
    test_type = quiz.keystroke_test_type

    student.save()

    keystroke_session = KeystrokeTestSession(student = student, test_type = test_type, timing_matrix = timing_matrix)
    keystroke_session.save()

    return Response({"student_id": student.id})


class StudentRudView(generics.RetrieveUpdateDestroyAPIView):
  lookup_field = 'pk'
  serializer_class = StudentSerializer

  def get_queryset(self):
    return Student.objects.all()
