# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='email',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='lastname',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='password',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='pseudo',
        ),
        migrations.AddField(
            model_name='staff',
            name='user',
            field=models.OneToOneField(default='noone', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
