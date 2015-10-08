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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score1', models.IntegerField(null=True)),
                ('score2', models.IntegerField(null=True)),
                ('court', models.ForeignKey(to='courts.Court')),
                ('team1', models.ForeignKey(related_name='team1', to='players.Pair')),
                ('team2', models.ForeignKey(related_name='team2', to='players.Pair')),
            ],
        ),
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='PoolMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match', models.ForeignKey(to='tournament.Match')),
                ('pool', models.ForeignKey(to='tournament.Pool')),
            ],
        ),
        migrations.CreateModel(
            name='PoolParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant', models.ForeignKey(to='players.Pair')),
                ('pool', models.ForeignKey(to='tournament.Pool')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('category', models.CharField(max_length=64)),
                ('pool_size', models.IntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='TournamentNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child1', models.ForeignKey(related_name='child1_', to='tournament.TournamentNode')),
                ('child2', models.ForeignKey(related_name='child2_', to='tournament.TournamentNode')),
                ('match', models.ForeignKey(to='tournament.Match')),
                ('parent', models.ForeignKey(related_name='parent_', to='tournament.TournamentNode')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
            field=models.ForeignKey(null=True, to='players.Pair'),
        ),
    ]
