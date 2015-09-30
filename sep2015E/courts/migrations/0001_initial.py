# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Court',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('owner', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=64)),
                ('zipcode', models.IntegerField(default=0)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=32)),
                ('ground', models.CharField(max_length=128)),
                ('cover', models.BooleanField(default=False)),
                ('image', models.FileField(upload_to='', null=True)),
                ('comment_access', models.TextField(default='')),
                ('comment_desiderata', models.TextField(default='')),
            ],
        ),
    ]
