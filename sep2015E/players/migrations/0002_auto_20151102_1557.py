# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import players.models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pair',
            name='average',
            field=models.DecimalField(max_digits=2, decimal_places=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(unique=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='user',
            name='firstname',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='user',
            name='lastname',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(validators=[players.models.User._phone_validator], max_length=32),
        ),
        migrations.AlterField(
            model_name='user',
            name='zipcode',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userregistration',
            name='level',
            field=models.DecimalField(max_digits=2, decimal_places=1),
        ),
    ]
