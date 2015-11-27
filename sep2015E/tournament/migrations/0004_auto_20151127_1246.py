# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0003_auto_20151127_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='mixte',
            field=models.CharField(choices=[('M', 'masculin'), ('F', 'féminin'), ('Mixte', 'mixte')], default='Mixte', max_length=16),
        ),
    ]
