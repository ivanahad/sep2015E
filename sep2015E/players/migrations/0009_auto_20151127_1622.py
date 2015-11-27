# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0008_auto_20151127_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregistration',
            name='payement_method',
            field=models.CharField(max_length=32, choices=[('Cash', 'Cash'), ('Visa', 'Visa'), ('Bancontact', 'Bancontact'), ('MasterCard', 'MasterCard'), ('Paypal', 'Paypal')]),
        ),
    ]
