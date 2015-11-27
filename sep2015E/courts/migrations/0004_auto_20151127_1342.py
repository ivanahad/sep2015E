# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0003_auto_20151123_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='court',
            name='zipcode',
            field=models.IntegerField(),
        ),
    ]
