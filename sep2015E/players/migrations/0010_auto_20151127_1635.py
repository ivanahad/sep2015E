# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0009_auto_20151127_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregistration',
            name='payement_method',
            field=models.CharField(default='Cash', max_length=32),
        ),
    ]
