# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0008_court_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='court',
            name='available',
            field=models.CharField(max_length=64, choices=[('Samedi', 'Samedi'), ('Dimanche', 'Dimanche'), ('Samedi et dimanche', 'Samedi et dimanche')]),
        ),
    ]
