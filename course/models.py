# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from keystroke.models import KeystrokeTestType
from django.contrib.auth.models import *

# Create your models here.
class Course(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=200)
  keystroke_test_type = models.ForeignKey(KeystrokeTestType, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.name)
