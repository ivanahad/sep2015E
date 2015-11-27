# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0002_auto_20151125_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='mixte',
            field=models.CharField(default='Mixte', max_length=16),
        ),
    ]
