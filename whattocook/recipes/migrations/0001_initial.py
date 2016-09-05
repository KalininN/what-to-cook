# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-05 17:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=500)),
                ('plates', models.IntegerField(default=1)),
            ],
        ),
    ]
