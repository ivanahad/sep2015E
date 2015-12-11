# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0012_auto_20151127_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='log',
            field=models.TextField(blank=True, default=''),
        ),
    ]
