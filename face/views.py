# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import generics, mixins
import json

from student.models import Student
from .detector import Detector

class FaceDistanceAPIView(generics.ListAPIView):

  def post(self, request, *args, **kwargs):

    user = request.POST.get('user_id')
    face_image_path = Student.objects.filter(moodle_username=user)[0].face_image.path
    current_image_path = request.FILES['current_image'].temporary_file_path()
    test_type_id = request.POST.get('test_type')

    d = Detector(face_image_path, current_image_path)
    
    return Response({
      'moodle_username': user,
      'distance': d.get_distance()
    })
