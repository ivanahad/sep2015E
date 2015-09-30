# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0002_user_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRegistration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('year', models.IntegerField(default=2015)),
                ('payment_method', models.CharField(max_length=64)),
                ('payment_done', models.BooleanField(default=False)),
                ('activities', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=128),
        ),
        migrations.AddField(
            model_name='userregistration',
            name='user',
            field=models.ForeignKey(to='players.User'),
        ),
    ]
