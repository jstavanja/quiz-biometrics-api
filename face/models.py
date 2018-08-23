# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from student.models import Student
from quiz.models import Quiz

# Create your models here.
class FaceComparisonResult(models.Model):
  quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  distance = models.FloatField()

  def __str__(self):
    return "Student: " + str(self.student) + " @ " + str(self.quiz_id) + ", Distance: " + str(self.distance)
