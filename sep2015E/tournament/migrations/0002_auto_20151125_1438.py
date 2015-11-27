# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='mixte',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='category',
            field=models.CharField(default='pré-minimes', choices=[('preminimes', 'pré-minimes'), ('minimes', 'minimes'), ('cadet', 'cadet'), ('scolaire', 'scolaire'), ('junior', 'junior'), ('seniores', 'seniors'), ('elites', 'elites'), ('familles', 'tournoi des familles')], max_length=64),
        ),
    ]
