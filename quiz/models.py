# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import *

import datetime

class Quiz(models.Model):
  quiz_owner = models.ForeignKey(User, unique=False, null=True)
  keystroke_test_type = models.ForeignKey('keystroke.KeystrokeTestType', on_delete = models.CASCADE)
  title = models.CharField(max_length=100)
  description = models.CharField(max_length=5000)
  date_of_quiz = models.DateField(default=datetime.date.today)

  def get_keystroke_test_type(self):
    return KeystrokeTestType.objects.filter(id=self.keystroke_test_type.id)

  def __str__(self):
    return str(self.title) + " @ " + str(self.date_of_quiz)
