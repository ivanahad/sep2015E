# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0005_auto_20151123_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pair',
            name='payment_done',
        ),
        migrations.RemoveField(
            model_name='pair',
            name='payment_method',
        ),
        migrations.AddField(
            model_name='user',
            name='payement_method',
            field=models.CharField(max_length=32, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='zipcode',
            field=models.IntegerField(),
        ),
    ]
