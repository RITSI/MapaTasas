# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-13 20:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasas', '0018_auto_20160911_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='actual',
            field=models.BooleanField(default=False),
        ),
    ]
