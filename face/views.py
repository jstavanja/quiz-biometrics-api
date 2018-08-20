# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import generics, mixins

from student.models import Student
# from .detector import Detector

class FaceDistanceAPIView(generics.ListAPIView):

  def post(self, request, *args, **kwargs):

    face_image_path = Student.objects.filter(moodle_username=request.POST.get('moodle_username'))[0].face_image.path
    current_image_path = request.FILES['current_image'].temporary_file_path()

    test_type_id = request.POST.get('test_type')

    # TODO: dockerize this app with the openface docker image

    # d = Detector(face_image, request.FILES.current_image.temporary_file_path())
    
    return Response({
      'moodle_username': request.POST.get('moodle_username'),
      'distance': 'TODO'
    })
