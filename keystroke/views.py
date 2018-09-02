# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect

from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from student.models import Student
from .models import KeystrokeTestType, KeystrokeTestSession, KeystrokeTestComparisonResult
from quiz.models import Quiz
from .serializers import KeystrokeTestTypeSerializer, KeystrokeTestSessionSerializer
from .forms import KeystrokeTestTypeForm

from .detector import Detector


class KeystrokeTestTypeAPIView(mixins.CreateModelMixin, generics.RetrieveUpdateDestroyAPIView):
  lookup_field = 'pk'
  serializer_class = KeystrokeTestTypeSerializer

  def get_queryset(self):
    return KeystrokeTestType.objects.all()

  def perform_create(self, serializer):
    serializer.save()

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)


class KeystrokeTestSessionAPIView(mixins.CreateModelMixin, generics.ListAPIView):
  lookup_field = 'pk'
  serializer_class = KeystrokeTestSessionSerializer

  def get_queryset(self):
    return KeystrokeTestSession.objects.all()

  def perform_create(self, serializer):
    serializer.save()

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)


class KeystrokeTestDistanceAPIView(generics.ListAPIView):

  renderer_classes = (JSONRenderer, )

  def post(self, request, *args, **kwargs):
    # dont do anything if user already has submitted this test
    req = json.loads(request.body.decode('utf-8'))
    user = Student.objects.filter(moodle_username=req['moodle_username'])[0]
    user_id = user.id
    quiz = Quiz.objects.filter(id=req['quiz_id'])[0]
    test_type_id = quiz.course.keystroke_test_type.id
    test_type = KeystrokeTestType.objects.filter(id=test_type_id)[0]

    print "test"
    
    original_matrix = json.loads(KeystrokeTestSession.objects.filter(student=user_id, test_type=test_type_id)[0].timing_matrix)
    current_matrix = req['current_matrix']

    # calculate distance using detector.py
    d = Detector(original_matrix, current_matrix)
    distance = d.get_euclidean_distance()

    result = KeystrokeTestComparisonResult(quiz_id = quiz,student = user, test_type = test_type, distance = distance)
    result.save()
    
    return Response({
      'distance': distance,
      'moodle_username': user_id,
      'current_matrix': current_matrix
    })

class KeystrokeTestTypeAdd(LoginRequiredMixin, FormMixin, TemplateView):
  model = KeystrokeTestType
  template_name = "keystroke_test_type_add.html"
  form_class = KeystrokeTestTypeForm

  def post(self , request , *args , **kwargs):
    form = self.get_form()
    if form.is_valid():
      instance = form.save(commit=False)
      instance.owner = self.request.user
      instance.save()
      return HttpResponseRedirect("/dash/keystroke_test/list")
    else:
      return self.form_invalid(form)


class KeystrokeTestTypeList(LoginRequiredMixin, TemplateView):
  template_name = "keystroke_test_type_list.html"

  def get_context_data(self, **kwargs):
    context = super(KeystrokeTestTypeList, self).get_context_data(**kwargs)
    context["test_types"] = KeystrokeTestType.objects.filter(owner = self.request.user).values()
    return context

class KeystrokeTestTypeUpdate(LoginRequiredMixin, UpdateView):
  template_name = "keystroke_test_type_update.html"
  fields = ['input_text', 'repetitions']
  success_url = '/dash/keystroke_test/list'

  def get_queryset(self):
    return KeystrokeTestType.objects.filter(owner=self.request.user)

class KeystrokeTestTypeIndex(LoginRequiredMixin, TemplateView):
  template_name = "keystroke_test_type_index.html"
  def get_context_data(self, **kwargs):
    context = super(KeystrokeTestTypeIndex, self).get_context_data(**kwargs)
    context["test_types"] = KeystrokeTestType.objects.filter(owner = self.request.user).order_by('-id')[:10].values()
    return context

