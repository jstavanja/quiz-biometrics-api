# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import KeystrokeTestType, KeystrokeTestSession

admin.site.register(KeystrokeTestType)
admin.site.register(KeystrokeTestSession)
