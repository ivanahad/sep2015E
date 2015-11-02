# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=128)),
                ('destinator', models.CharField(max_length=128)),
                ('title', models.CharField(max_length=128)),
                ('message', models.TextField(default='', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=64)),
                ('country', models.CharField(max_length=64)),
                ('zipcode', models.IntegerField(default=0)),
                ('phone', models.CharField(max_length=32)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
