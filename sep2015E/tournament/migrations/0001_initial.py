# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '__first__'),
        ('courts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('score1', models.IntegerField(null=True, blank=True)),
                ('score2', models.IntegerField(null=True, blank=True)),
                ('court', models.ForeignKey(blank=True, to='courts.Court', null=True)),
                ('team1', models.ForeignKey(related_name='team1', to='players.Pair')),
                ('team2', models.ForeignKey(related_name='team2', to='players.Pair')),
            ],
        ),
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('number', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PoolMatch',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('match', models.ForeignKey(to='tournament.Match')),
                ('pool', models.ForeignKey(to='tournament.Pool')),
            ],
        ),
        migrations.CreateModel(
            name='PoolParticipant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('participant', models.ForeignKey(to='players.Pair')),
                ('pool', models.ForeignKey(to='tournament.Pool')),
            ],
        ),
        migrations.CreateModel(
            name='SoloParticipant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('player', models.ForeignKey(to='players.User')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=64)),
                ('category', models.CharField(max_length=64)),
                ('pool_size', models.IntegerField(default=5)),
                ('is_open', models.BooleanField(default=True)),
                ('season', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ['name', 'category'],
            },
        ),
        migrations.CreateModel(
            name='TournamentNode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('child1', models.ForeignKey(to='tournament.TournamentNode', blank=True, related_name='child1_', null=True)),
                ('child2', models.ForeignKey(to='tournament.TournamentNode', blank=True, related_name='child2_', null=True)),
                ('match', models.ForeignKey(to='tournament.Match')),
                ('parent', models.ForeignKey(to='tournament.TournamentNode', blank=True, related_name='parent_', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TournamentParticipant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('participant', models.ForeignKey(to='players.Pair')),
                ('tournament', models.ForeignKey(to='tournament.Tournament')),
            ],
        ),
        migrations.AddField(
            model_name='tournament',
            name='k_o_root',
            field=models.ForeignKey(blank=True, to='tournament.TournamentNode', null=True),
        ),
        migrations.AddField(
            model_name='soloparticipant',
            name='tournament',
            field=models.ForeignKey(to='tournament.Tournament'),
        ),
        migrations.AddField(
            model_name='pool',
            name='tournament',
            field=models.ForeignKey(to='tournament.Tournament'),
        ),
        migrations.AddField(
            model_name='pool',
            name='winner',
            field=models.ForeignKey(blank=True, to='players.Pair', null=True),
        ),
    ]
