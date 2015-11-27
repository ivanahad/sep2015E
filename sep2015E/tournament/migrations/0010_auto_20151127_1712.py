# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0009_pool_court'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pool',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
