# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-20 16:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KeystrokeTestSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timing_matrix', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='KeystrokeTestType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_text', models.CharField(max_length=5000)),
                ('repetitions', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moodle_username', models.CharField(max_length=250)),
                ('path_to_image', models.CharField(max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name='keystroketestsession',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keystroke.Student'),
        ),
        migrations.AddField(
            model_name='keystroketestsession',
            name='test_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keystroke.KeystrokeTestType'),
        ),
    ]
