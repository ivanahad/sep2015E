# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Court',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('owner', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=64)),
                ('zipcode', models.IntegerField(default=0)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=32)),
                ('ground', models.CharField(max_length=128)),
                ('cover', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to='', blank=True)),
                ('comment_access', models.TextField(default='')),
                ('comment_desiderata', models.TextField(default='')),
                ('available', models.BooleanField(default=True)),
            ],
        ),
    ]
