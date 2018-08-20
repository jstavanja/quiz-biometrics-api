# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins

from student.models import Student
from student.serializers import StudentSerializer

class StudentAPIView(mixins.CreateModelMixin, generics.ListAPIView):
  lookup_field = 'pk'
  serializer_class = StudentSerializer

  def get_queryset(self):
    return Student.objects.all()

  def perform_create(self, serializer):
    serializer.save()

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)


class StudentRudView(generics.RetrieveUpdateDestroyAPIView):
  lookup_field = 'pk'
  serializer_class = StudentSerializer

  def get_queryset(self):
    return Student.objects.all()
