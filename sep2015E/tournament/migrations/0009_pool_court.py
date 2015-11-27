# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0004_auto_20151127_1342'),
        ('tournament', '0008_auto_20151127_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='pool',
            name='court',
            field=models.ForeignKey(null=True, to='courts.Court'),
        ),
    ]
