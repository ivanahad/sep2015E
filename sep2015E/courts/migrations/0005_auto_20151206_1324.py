# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0004_auto_20151127_1342'),
    ]

    operations = [
        migrations.RenameField(
            model_name='court',
            old_name='owner',
            new_name='owner_firstname',
        ),
        migrations.AddField(
            model_name='court',
            name='owner_lastname',
            field=models.CharField(max_length=128, default=datetime.datetime(2015, 12, 6, 12, 24, 43, 192949, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='court',
            name='ground',
            field=models.CharField(max_length=128, choices=[('brique', 'Brique'), ('beton', 'Béton'), ('synthetique', 'Synthétique'), ('terre battue', 'Terre battue'), ('quick', 'Quick'), ('autres', 'Autres')], default='autres'),
        ),
    ]
