# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '__first__'),
        ('players', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('score1', models.IntegerField(null=True, blank=True)),
                ('score2', models.IntegerField(null=True, blank=True)),
                ('court', models.ForeignKey(null=True, blank=True, to='courts.Court')),
                ('team1', models.ForeignKey(to='players.Pair', related_name='team1')),
                ('team2', models.ForeignKey(to='players.Pair', related_name='team2')),
            ],
        ),
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('number', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PoolMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('match', models.ForeignKey(to='tournament.Match')),
                ('pool', models.ForeignKey(to='tournament.Pool')),
            ],
        ),
        migrations.CreateModel(
            name='PoolParticipant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('participant', models.ForeignKey(to='players.Pair')),
                ('pool', models.ForeignKey(to='tournament.Pool')),
            ],
        ),
        migrations.CreateModel(
            name='SoloParticipant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('player', models.ForeignKey(to='players.User')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=64)),
                ('category', models.CharField(max_length=64)),
                ('pool_size', models.IntegerField(default=5)),
                ('is_open', models.BooleanField(default=True)),
                ('season', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ['category', 'name'],
            },
        ),
        migrations.CreateModel(
            name='TournamentNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('child1', models.ForeignKey(null=True, related_name='child1_', blank=True, to='tournament.TournamentNode')),
                ('child2', models.ForeignKey(null=True, related_name='child2_', blank=True, to='tournament.TournamentNode')),
                ('match', models.ForeignKey(to='tournament.Match')),
                ('parent', models.ForeignKey(null=True, related_name='parent_', blank=True, to='tournament.TournamentNode')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentParticipant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('participant', models.ForeignKey(to='players.Pair')),
                ('tournament', models.ForeignKey(to='tournament.Tournament')),
            ],
        ),
        migrations.AddField(
            model_name='tournament',
            name='k_o_root',
            field=models.ForeignKey(null=True, blank=True, to='tournament.TournamentNode'),
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
            field=models.ForeignKey(null=True, blank=True, to='players.Pair'),
        ),
    ]
