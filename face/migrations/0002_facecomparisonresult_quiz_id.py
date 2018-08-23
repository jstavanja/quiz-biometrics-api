# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-23 17:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20180823_1653'),
        ('face', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='facecomparisonresult',
            name='quiz_id',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='quiz.Quiz'),
            preserve_default=False,
        ),
    ]