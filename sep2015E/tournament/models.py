from django.db import models

class Tournament(models.Model):
    """This class defines a unique tournament.
    This includes some pools and one knock-off tree.
    """
    name = models.CharField(max_length=64) # p.ex. "Familles"
    category = models.CharField(max_length=64) # p.ex. "strongest"
    pool_size = models.IntegerField(default=5)
    k_o_root = models.ForeignKey('TournamentNode', null=True, blank=True)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return "%s %s" % (self.name, self.category)

class TournamentParticipant(models.Model):
    """Link between tournament.Tournament and players.Pair.
    """
    tournament = models.ForeignKey('Tournament')
    participant = models.ForeignKey('players.Pair')

    def __str__(self):
        return "%s: %s" % (self.tournament, self.participant)

class Pool(models.Model):
    """Defines a pool of players trying to qualify for the
    knock-off tournament.
    """
    tournament = models.ForeignKey('Tournament')
    number = models.IntegerField(default=0, blank=True)
    size = models.IntegerField(default=5)
    winner = models.ForeignKey('players.Pair', null=True, blank=True)

    def __str__(self):
        return "%s - pool %d" % (self.tournament, self.number)

class PoolParticipant(models.Model):
    """Link between tournament.Pool and players.Pair.
    """
    pool = models.ForeignKey('Pool')
    participant = models.ForeignKey('players.Pair')

    def __str__(self):
        return "%s: %s" % (self.pool, self.participant)

class Match(models.Model):
    """Defines a match between two teams."""
    team1 = models.ForeignKey('players.Pair', related_name='team1')
    team2 = models.ForeignKey('players.Pair', related_name='team2')
    score1 = models.IntegerField(null=True, blank=True)
    score2 = models.IntegerField(null=True, blank=True)
    court = models.ForeignKey('courts.Court', null=True, blank=True)

    def __str__(self):
        return "%s vs %s" % (self.team1, self.team2)

class PoolMatch(models.Model):
    """Link between tournament.Pool and tournament.Match.
    """
    pool = models.ForeignKey('Pool')
    match = models.ForeignKey('Match')

    def __str__(self):
        return "%s: %s" % (self.pool, self.match)

class TournamentNode(models.Model):
    """Defines a node for the tree of a knock-off tournament.
    Value is the match (once the two players are known), rest
    is the recursive links.
    """
    match = models.ForeignKey('Match')
    parent = models.ForeignKey('self', related_name='parent_', blank=True, null=True)
    child1 = models.ForeignKey('self', related_name='child1_', blank=True, null=True)
    child2 = models.ForeignKey('self', related_name='child2_', blank=True, null=True)

