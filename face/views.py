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
from .models import FaceComparisonResult
from quiz.models import Quiz

class FaceDistanceAPIView(generics.ListAPIView):

  def post(self, request, *args, **kwargs):

    # dont do anything if user already has submitted this test 
    user = request.POST.get('user_id')
    student = Student.objects.filter(moodle_username=user)[0]
    face_image_path = student.face_image.path
    current_image_path = request.FILES['current_image'].temporary_file_path()
    quiz = Quiz.objects.filter(id=request.POST.get('quiz_id'))[0]

    d = Detector(face_image_path, current_image_path)
    distance = d.get_distance()

    result = FaceComparisonResult(quiz_id = quiz,student = student, distance = distance)
    result.save()
    
    return Response({
      'moodle_username': user,
      'distance': distance
    })
