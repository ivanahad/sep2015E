# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '__first__'),
        ('courts', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('score1', models.IntegerField(null=True)),
                ('score2', models.IntegerField(null=True)),
                ('court', models.ForeignKey(to='courts.Court')),
                ('team1', models.ForeignKey(to='players.Pair', related_name='team1')),
                ('team2', models.ForeignKey(to='players.Pair', related_name='team2')),
            ],
        ),
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('size', models.IntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='PoolMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('match', models.ForeignKey(to='tournament.Match')),
                ('pool', models.ForeignKey(to='tournament.Pool')),
            ],
        ),
        migrations.CreateModel(
            name='PoolParticipant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('participant', models.ForeignKey(to='players.Pair')),
                ('pool', models.ForeignKey(to='tournament.Pool')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('category', models.CharField(max_length=64)),
                ('pool_size', models.IntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='TournamentNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('child1', models.ForeignKey(to='tournament.TournamentNode', related_name='child1_')),
                ('child2', models.ForeignKey(to='tournament.TournamentNode', related_name='child2_')),
                ('match', models.ForeignKey(to='tournament.Match')),
                ('parent', models.ForeignKey(to='tournament.TournamentNode', related_name='parent_')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentParticipant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('participant', models.ForeignKey(to='players.Pair')),
                ('tournament', models.ForeignKey(to='tournament.Tournament')),
            ],
        ),
        migrations.AddField(
            model_name='tournament',
            name='k_o_root',
            field=models.ForeignKey(to='tournament.TournamentNode'),
        ),
        migrations.AddField(
            model_name='pool',
            name='tournament',
            field=models.ForeignKey(to='tournament.Tournament'),
        ),
        migrations.AddField(
            model_name='pool',
            name='winner',
            field=models.ForeignKey(to='players.Pair', null=True),
        ),
    ]
