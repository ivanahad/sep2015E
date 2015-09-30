# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pair',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('average', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('firstname', models.CharField(max_length=128)),
                ('lastname', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=64)),
                ('country', models.CharField(max_length=64)),
                ('zipcode', models.IntegerField(default=0)),
                ('email', models.CharField(max_length=128)),
                ('level', models.CharField(max_length=8)),
            ],
        ),
        migrations.AddField(
            model_name='pair',
            name='player1',
            field=models.ForeignKey(to='players.User', related_name='player1'),
        ),
        migrations.AddField(
            model_name='pair',
            name='player2',
            field=models.ForeignKey(to='players.User', related_name='player2'),
        ),
    ]
