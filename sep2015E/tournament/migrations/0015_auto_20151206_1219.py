# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0014_auto_20151203_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='category',
            field=models.CharField(default='pré-minimes', choices=[('preminimes', 'pré-minimes'), ('minimes', 'minimes'), ('cadets', 'cadets'), ('scolaires', 'scolaires'), ('junior', 'junior'), ('seniores', 'seniors'), ('elites', 'elites'), ('familles', 'tournoi des familles')], max_length=64),
        ),
    ]
