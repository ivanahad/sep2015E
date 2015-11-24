# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0002_auto_20151113_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='court',
            name='ground',
            field=models.CharField(default='autres', choices=[('brique', 'brique'), ('beton', 'béton'), ('synthetique', 'synthétique'), ('terre battue', 'terre battue'), ('quick', 'quick'), ('autres', 'autres')], max_length=128),
        ),
    ]
