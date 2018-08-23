# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from student.models import Student

class KeystrokeTestType(models.Model):
  input_text = models.CharField(max_length=5000)
  repetitions = models.IntegerField()

  def __str__(self):
    return self.input_text + ' -> reps: ' + str(self.repetitions)


class KeystrokeTestSession(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  test_type = models.ForeignKey(KeystrokeTestType, on_delete=models.CASCADE)
  timing_matrix = models.CharField(max_length=5000)

  def __str__(self):
    return "Student: " + str(self.student) + ", Test type: " + str(self.test_type)


class KeystrokeTestComparisonResult(models.Model):
  quiz_id = models.ForeignKey('quiz.Quiz', on_delete=models.CASCADE)
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  test_type = models.ForeignKey(KeystrokeTestType)
  distance = models.FloatField()

  def __str__(self):
    return "Student: " + str(self.student) + ", Distance: " + str(self.distance)
