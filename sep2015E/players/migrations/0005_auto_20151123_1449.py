# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0004_auto_20151112_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregistration',
            name='level',
            field=models.CharField(choices=[('C30.5', 'C30.5'), ('C30.4', 'C30.4'), ('C30.3', 'C30.3'), ('C30.2', 'C30.2'), ('C30.1', 'C30.1'), ('C30', 'C30'), ('C15.5', 'C15.5'), ('C15.4', 'C15.4'), ('C15.3', 'C15.3'), ('C15.2', 'C15.2'), ('C15.1', 'C15.1'), ('C15', 'C15'), ('B+4/6', 'B+4/6'), ('B+2/6', 'B+2/6'), ('B0', 'B0'), ('B-2/6', 'B-2/6'), ('B-4/6', 'B-4/6'), ('B-15', 'B-15'), ('B-15.1', 'B-15.1'), ('B-15.2', 'B-15.2'), ('B-15.4', 'B-15.4'), ('A4', 'A4'), ('A3', 'A3'), ('A2', 'A2'), ('A1', 'A1')], max_length=32),
        ),
    ]
