# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0005_pool_leader'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 27, 14, 17, 24, 81831, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
