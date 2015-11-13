# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pair',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('average', models.IntegerField(default=0)),
                ('season', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('firstname', models.CharField(max_length=128, blank=True)),
                ('lastname', models.CharField(max_length=128, blank=True)),
                ('address', models.CharField(max_length=128, blank=True)),
                ('city', models.CharField(max_length=64, blank=True)),
                ('country', models.CharField(max_length=64, blank=True)),
                ('zipcode', models.IntegerField(default=0, blank=True)),
                ('email', models.EmailField(max_length=128, blank=True)),
                ('phone', models.CharField(max_length=32, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('season', models.CharField(max_length=32)),
                ('payment_method', models.CharField(default=('Cash', 'Cash'), max_length=64, choices=[('Cash', 'Cash'), ('Visa', 'Visa'), ('Bancontact', 'Bancontact'), ('MasterCard', 'MasterCard'), ('Paypal', 'Paypal')])),
                ('payment_done', models.BooleanField(default=False)),
                ('bbq', models.BooleanField(default=False)),
                ('activities', models.TextField(max_length=2048, blank=True)),
                ('comment', models.TextField(default='', max_length=2048, blank=True)),
                ('level', models.CharField(max_length=8, blank=True)),
                ('user', models.ForeignKey(to='players.User')),
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
