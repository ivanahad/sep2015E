# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0007_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='court',
            name='log',
            field=models.TextField(blank=True, default=''),
        ),
    ]
