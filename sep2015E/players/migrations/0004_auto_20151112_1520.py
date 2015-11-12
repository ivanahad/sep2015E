# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import players.models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0003_auto_20151111_1018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='address',
            new_name='address_street',
        ),
        migrations.RemoveField(
            model_name='userregistration',
            name='activities',
        ),
        migrations.RemoveField(
            model_name='userregistration',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='userregistration',
            name='payment_done',
        ),
        migrations.RemoveField(
            model_name='userregistration',
            name='payment_method',
        ),
        migrations.AddField(
            model_name='pair',
            name='comment',
            field=models.TextField(default='', max_length=2048, blank=True),
        ),
        migrations.AddField(
            model_name='pair',
            name='payment_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pair',
            name='payment_method',
            field=models.CharField(default=('Cash', 'Cash'), choices=[('Cash', 'Cash'), ('Visa', 'Visa'), ('Bancontact', 'Bancontact'), ('MasterCard', 'MasterCard'), ('Paypal', 'Paypal')], max_length=64),
        ),
        migrations.AddField(
            model_name='user',
            name='address_box',
            field=models.CharField(max_length=8, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='address_number',
            field=models.CharField(default=42, max_length=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='birthdate',
            field=models.DateField(default="2015-11-12"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(default='M', choices=[('M', 'Homme'), ('F', 'Femme')], max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=32, validators=[players.models.User._phone_validator]),
        ),
    ]
