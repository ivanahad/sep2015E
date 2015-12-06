# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0005_auto_20151206_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='court',
            name='ground',
            field=models.CharField(default='autres', max_length=128, choices=[('Brique', 'Brique'), ('Béton', 'Béton'), ('Synthetique', 'Synthétique'), ('Terre battue', 'Terre battue'), ('Quick', 'Quick'), ('Autres', 'Autres')]),
        ),
    ]
