# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import inspect
from rest_framework import status
from django.shortcuts import render
from django.views.generic.base import TemplateView

from .serializers import QuizSerializer
from keystroke.serializers import KeystrokeTestTypeSerializer
from .models import Quiz
from keystroke.models import KeystrokeTestType, KeystrokeTestComparisonResult
from face.models import FaceComparisonResult
from student.models import Student

class QuizInfoAPIView(generics.RetrieveUpdateDestroyAPIView):
  lookup_field = 'pk'
  serializer_class = QuizSerializer

  def get_queryset(self):
    return Quiz.objects.all()

class DashQuizList(TemplateView):
  template_name = "quizzes.html"

  def get_context_data(self, **kwargs):
    context = super(DashQuizList, self).get_context_data(**kwargs)
    context["quizzes"] = Quiz.objects.all().values()
    return context

class DashQuizResult(LoginRequiredMixin, TemplateView):
  template_name = "quiz.html"

  def get_context_data(self, **kwargs):
    context = super(DashQuizResult, self).get_context_data(**kwargs)
    quiz_id = self.kwargs['pk']
    context["quiz"] = Quiz.objects.filter(id=quiz_id)[0]

    results = {}

    # find keystroke results from this quiz
    keystroke_results = KeystrokeTestComparisonResult.objects.filter(quiz_id=quiz_id)

    # find faceresuts with from this quiz
    face_results = FaceComparisonResult.objects.filter(quiz_id=quiz_id)

    # map them in one object to user ids
    for result in keystroke_results:
      student = Student.objects.filter(id=result.student_id)[0]
      
      if (results.get(student.moodle_username) is None):
        results[student.moodle_username] = {}
      results[student.moodle_username]['keystroke'] = result.distance

    for result in face_results:
      student = Student.objects.filter(id=result.student_id)[0]

      if (results.get(student.moodle_username) is None):
        results[student.moodle_username] = {}
      results[student.moodle_username]['face'] = result.distance

    context["result_iteritems"] = results.iteritems()

    return context
