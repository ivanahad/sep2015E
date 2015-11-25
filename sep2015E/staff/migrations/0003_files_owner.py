# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='owner',
            field=models.ForeignKey(to='staff.Staff', default=None),
            preserve_default=False,
        ),
    ]
