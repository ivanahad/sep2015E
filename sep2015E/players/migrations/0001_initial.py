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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('average', models.IntegerField(default=0)),
                ('season', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('firstname', models.CharField(blank=True, max_length=128)),
                ('lastname', models.CharField(blank=True, max_length=128)),
                ('address', models.CharField(blank=True, max_length=128)),
                ('city', models.CharField(blank=True, max_length=64)),
                ('country', models.CharField(blank=True, max_length=64)),
                ('zipcode', models.IntegerField(default=0, blank=True)),
                ('email', models.EmailField(blank=True, max_length=128)),
                ('phone', models.CharField(blank=True, max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='UserRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('season', models.CharField(max_length=32)),
                ('payment_method', models.CharField(default=('Cash', 'Cash'), choices=[('Cash', 'Cash'), ('Visa', 'Visa'), ('Bancontact', 'Bancontact'), ('MasterCard', 'MasterCard'), ('Paypal', 'Paypal')], max_length=64)),
                ('payment_done', models.BooleanField(default=False)),
                ('bbq', models.BooleanField(default=False)),
                ('activities', models.TextField(blank=True, max_length=2048)),
                ('comment', models.TextField(default='', blank=True, max_length=2048)),
                ('level', models.CharField(blank=True, max_length=8)),
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
