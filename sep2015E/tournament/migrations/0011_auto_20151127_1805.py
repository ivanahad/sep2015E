# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0010_auto_20151127_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pool',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
