from django.db import models

class Tournament(models.Model):
    """This class defines a unique tournament.
    This includes some pools and one knock-off tree.
    """
    name = models.CharField(max_length=64) # p.ex. "Familles"
    category = models.CharField(max_length=64) # p.ex. "strongest"
    pool_size = models.IntegerField(default=5)
    k_o_root = models.ForeignKey('TournamentNode')

class TournamentParticipant(models.Model):
    """Link between tournament.Tournament and players.Pair.
    """
    tournament = models.ForeignKey('Tournament')
    participant = models.ForeignKey('players.Pair')

class Pool(models.Model):
    """Defines a pool of players trying to qualify for the
    knock-off tournament.
    """
    tournament = models.ForeignKey('Tournament')
    size = models.IntegerField(default=5)
    winner = models.ForeignKey('players.Pair', null=True)

class PoolParticipant(models.Model):
    """Link between tournament.Pool and players.Pair.
    """
    pool = models.ForeignKey('Pool')
    participant = models.ForeignKey('players.Pair')

class Match(models.Model):
    """Defines a match between two teams."""
    team1 = models.ForeignKey('players.Pair', related_name='team1')
    team2 = models.ForeignKey('players.Pair', related_name='team2')
    score1 = models.IntegerField(null=True)
    score2 = models.IntegerField(null=True)
    court = models.ForeignKey('courts.Court')

class PoolMatch(models.Model):
    """Link between tournament.Pool and tournament.Match.
    """
    pool = models.ForeignKey('Pool')
    match = models.ForeignKey('Match')

class TournamentNode(models.Model):
    """Defines a node for the tree of a knock-off tournament.
    Value is the match (once the two players are known), rest
    is the recursive links.
    """
    match = models.ForeignKey('Match')
    parent = models.ForeignKey('self', related_name='parent_')
    child1 = models.ForeignKey('self', related_name='child1_')
    child2 = models.ForeignKey('self', related_name='child2_')

