# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.views.generic.base import TemplateView

from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from .serializers import QuizSerializer
from keystroke.serializers import KeystrokeTestTypeSerializer
from .models import Quiz
from keystroke.models import KeystrokeTestType, KeystrokeTestComparisonResult
from face.models import FaceComparisonResult
from student.models import Student

from .forms import QuizForm, QuizFormSet

class QuizInfoAPIView(generics.RetrieveUpdateDestroyAPIView):
  lookup_field = 'pk'
  serializer_class = QuizSerializer

  def get_queryset(self):
    return Quiz.objects.all()

# TODO: display only quizzes that the current user has created

class DashQuiz(LoginRequiredMixin, TemplateView):
  template_name = "quiz_index.html"


class DashQuizList(LoginRequiredMixin, TemplateView):
  template_name = "quiz_list.html"

  def get_context_data(self, **kwargs):
    context = super(DashQuizList, self).get_context_data(**kwargs)
    context["quizzes"] = Quiz.objects.filter(quiz_owner = self.request.user).values()
    return context

class DashQuizResult(LoginRequiredMixin, TemplateView):
  template_name = "quiz_details.html"

  def get_context_data(self, **kwargs):


    context = super(DashQuizResult, self).get_context_data(**kwargs)
    quiz_id = self.kwargs['pk']
    quiz = Quiz.objects.filter(id=quiz_id)[0]

    if quiz.quiz_owner != self.request.user:
      raise Http404

    context["quiz"] = quiz

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
    
    keystroke_distances = [value['keystroke'] for key, value in results.iteritems()]
    face_distances = [value['face'] for key, value in results.iteritems()]
    if len(keystroke_distances) > 0:
      context["avg_keystroke_distance"] = sum(keystroke_distances)/len(keystroke_distances)
    else:
      context["avg_keystroke_distance"] = 0
    
    if len(face_distances) > 0:
      context["avg_face_distance"] = sum(face_distances)/len(face_distances)
    else:
      context["avg_face_distance"] = 0

    return context

class DashQuizAdd(LoginRequiredMixin, FormMixin, TemplateView):
  model = Quiz
  template_name = "quiz_add.html"
  form_class = QuizForm

  def get_form_kwargs(self):
    kwargs = super(DashQuizAdd, self).get_form_kwargs()
    kwargs.update({'owner': self.request.user})
    return kwargs

  def post(self , request , *args , **kwargs):
    form = self.get_form()
    if form.is_valid():
      instance = form.save(commit=False)
      instance.quiz_owner = self.request.user
      instance.save()
      return HttpResponseRedirect("/dash/quiz/results")
    else:
      return self.form_invalid(form)

class Dash(LoginRequiredMixin, TemplateView):
  template_name = "dash_index.html"
    