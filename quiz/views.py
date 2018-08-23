# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from .serializers import QuizSerializer
from keystroke.serializers import KeystrokeTestTypeSerializer
from .models import Quiz
from keystroke.models import KeystrokeTestType

class QuizInfoAPIView(generics.RetrieveUpdateDestroyAPIView):
  lookup_field = 'pk'
  serializer_class = QuizSerializer

  def get_queryset(self):
    return Quiz.objects.all()
