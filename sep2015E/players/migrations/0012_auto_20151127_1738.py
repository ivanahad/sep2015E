# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0011_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregistration',
            name='payement_method',
            field=models.CharField(blank=True, choices=[('Cash', 'Cash'), ('Visa', 'Visa'), ('Bancontact', 'Bancontact'), ('MasterCard', 'MasterCard'), ('Paypal', 'Paypal')], max_length=32, default='Cash'),
        ),
    ]
