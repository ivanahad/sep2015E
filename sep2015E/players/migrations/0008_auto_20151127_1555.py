# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0007_auto_20151127_1501'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userregistration',
            old_name='payment_done',
            new_name='payement_done',
        ),
        migrations.RenameField(
            model_name='userregistration',
            old_name='payment_method',
            new_name='payement_method',
        ),
    ]
