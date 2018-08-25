# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import os

def face_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/
    image_name, image_format = os.path.splitext(filename)
    return 'user_{0}/face{1}'.format(instance.id, image_format)


class Student(models.Model):
  moodle_username = models.CharField(max_length=250)
  face_image = models.ImageField(upload_to=face_image_directory_path)

  # so we can use the face_image_directory_path function @ registration
  def save(self, *args, **kwargs):
    if self.pk is None:
      saved_image = self.face_image
      self.face_image = None
      super(Student, self).save(*args, **kwargs)
      self.face_image = saved_image

    super(Student, self).save(*args, **kwargs)

  def __str__(self):
    return self.moodle_username
