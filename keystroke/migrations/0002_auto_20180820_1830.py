# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-20 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keystroke', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='path_to_image',
        ),
        migrations.AddField(
            model_name='student',
            name='face_image',
            field=models.ImageField(default='https://via.placeholder.com/350x150', upload_to=b''),
            preserve_default=False,
        ),
    ]
