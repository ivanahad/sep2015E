# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0006_auto_20151126_2258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='payement_method',
        ),
        migrations.AddField(
            model_name='userregistration',
            name='payment_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userregistration',
            name='payment_method',
            field=models.CharField(max_length=32, blank=True),
        ),
    ]
