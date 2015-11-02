# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('author', models.CharField(max_length=128)),
                ('destinator', models.CharField(max_length=128)),
                ('title', models.CharField(max_length=128)),
                ('message', models.TextField(default='', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('firstname', models.CharField(max_length=128)),
                ('lastname', models.CharField(max_length=128)),
                ('pseudo', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=64)),
                ('country', models.CharField(max_length=64)),
                ('zipcode', models.IntegerField(default=0)),
                ('email', models.EmailField(max_length=128)),
                ('phone', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
    ]
