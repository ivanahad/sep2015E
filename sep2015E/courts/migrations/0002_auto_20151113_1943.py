# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import courts.models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='court',
            old_name='address',
            new_name='address_street',
        ),
        migrations.AddField(
            model_name='court',
            name='address_box',
            field=models.CharField(null=True, max_length=8, blank=True),
        ),
        migrations.AddField(
            model_name='court',
            name='address_number',
            field=models.CharField(max_length=8, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='court',
            name='owner_address_box',
            field=models.CharField(null=True, max_length=8, blank=True),
        ),
        migrations.AddField(
            model_name='court',
            name='owner_address_number',
            field=models.CharField(max_length=8, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='court',
            name='owner_address_street',
            field=models.CharField(max_length=128, default='st'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='court',
            name='comment_access',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='court',
            name='comment_desiderata',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='court',
            name='image',
            field=models.ImageField(upload_to='', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='court',
            name='phone',
            field=models.CharField(max_length=32, validators=[courts.models.Court._phone_validator]),
        ),
    ]
