# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from student.models import Student
from .models import KeystrokeTestType, KeystrokeTestSession
from .serializers import KeystrokeTestTypeSerializer, KeystrokeTestSessionSerializer

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

    req = json.loads(request.body.decode('utf-8'))
    user_id = Student.objects.filter(moodle_username=req['moodle_username'])[0].id
    test_type_id = req['test_type']

    print "test"
    
    original_matrix = json.loads(KeystrokeTestSession.objects.filter(student=user_id, test_type=test_type_id)[0].timing_matrix)
    current_matrix = req['current_matrix']

    # calculate distance using detector.py
    d = Detector(original_matrix, current_matrix)
    
    return Response({
      'distance': d.get_euclidean_distance(),
      'moodle_username': user_id,
      'current_matrix': current_matrix
    })

