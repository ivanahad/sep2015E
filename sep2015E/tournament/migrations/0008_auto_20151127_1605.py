# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0007_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='date',
        ),
        migrations.AddField(
            model_name='pool',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 27, 15, 5, 35, 696433, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
