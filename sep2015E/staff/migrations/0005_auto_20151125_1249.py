# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0004_auto_20151125_1220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='destinator',
        ),
        migrations.AlterField(
            model_name='messages',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='messages',
            name='message',
            field=models.TextField(default='', blank=True, max_length=2048),
        ),
    ]
