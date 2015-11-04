from django.db import models
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import players.models
import math

class Tournament(models.Model):
    """This class defines a unique tournament.
    This includes some pools and one knock-off tree.
    """
    name = models.CharField(max_length=64) # p.ex. "Familles"
    category = models.CharField(max_length=64) # p.ex. "strongest"
    pool_size = models.IntegerField(default=5)
    k_o_root = models.ForeignKey('TournamentNode', null=True, blank=True)
    is_open = models.BooleanField(default=True)
    season = models.CharField(max_length=32);

    class Meta:
        ordering = ['name', 'category']

    def close_registrations(self):
        if not self.is_open :
            raise Exception("Tournament is already closed.")

        # pair all solo participants if possible
        SoloParticipant.pairing(self)

        # list of players from database
        pairs = TournamentParticipant.objects.filter(tournament=self)
        pairs = [entry.participant for entry in pairs]

        nb_pools = math.ceil(len(pairs) / self.pool_size)
        pools = [Pool() for _ in range(nb_pools)]
        for i in range(len(pools)):
            pools[i].tournament = self
            pools[i].number = i
            pools[i].save()

        Tournament.assign_players(pools, pairs, self.pool_size)
        for pool in pools:
            pool.create_matches()

        self.is_open = False
        self.save()
        self.generate_pdf()

    def assign_players(pools, players, size):
        """Assign all the players in the pools, trying to match size
        as the size of the pools.
        The list players is empty at the end if the method was successful.

        Note: this method can be improved to match the players better,
        if the players list is sorted.
        """
        nb_reduced_pools = len(pools) * size - len(players)
        nb_standard_pools = len(pools) - nb_reduced_pools

        for i in range(len(pools)):
            for _ in range(size if i < nb_standard_pools else size - 1):
                pp = PoolParticipant()
                pp.pool = pools[i]
                pp.participant = players.pop()
                pp.save()

    def generate_pdf(self):
        """Generate the pdf showing the pools for a particular tournament (id_)"""
        doc = SimpleDocTemplate("pools.pdf", pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
        doc.pagesize = landscape(A4)
        elements = []

        style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                               ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                               ('VALIGN',(0,0),(0,-1),'TOP'),
                               ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                               ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                               ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                               ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                               ])

        #Configure style and word wrap
        s = getSampleStyleSheet()
        s = s["BodyText"]
        s.wordWrap = 'CJK'

        pools = Pool.objects.filter(tournament=self);

         #Generate a table in the pdf for all pools
        for pool in pools:
            participants = PoolParticipant.objects.filter(pool=pool) #List of participants
            data = [
            ["Id", "Noms", "Victoires", "Défaites"],
            ]
            for p in participants:
                row = [str(p.id), str(p), str(0), str(0)]
                data.append(row)
            data2 = [[Paragraph(cell, s) for cell in row] for row in data]
            t=Table(data2)
            t.setStyle(style)
            #Send the data
            elements.append(t)

        #Append the file
        p = doc.build(elements)


    def __str__(self):
        return "%s %s" % (self.name, self.category)

class TournamentParticipant(models.Model):
    """Link between tournament.Tournament and players.Pair.
    """
    tournament = models.ForeignKey('Tournament')
    participant = models.ForeignKey('players.Pair')

    def __str__(self):
        return "%s: %s" % (self.tournament, self.participant)

class SoloParticipant(models.Model):
    """Players registered without a pair for a tournament.
    """
    tournament = models.ForeignKey('Tournament')
    player = models.ForeignKey('players.User')

    def pairing(tournament):
        #matching of solo registrations
        solo = SoloParticipant.objects.filter(tournament=tournament)
        solo = [entry.player for entry in solo]

        i = 0
        while i < len(solo)-1 :
            new_pair = players.models.Pair( \
                    player1 = solo[i], \
                    player2 = solo[i+1], \
                    season = tournament.season)
            new_pair.save()

            registration = TournamentParticipant( \
                    tournament = tournament, \
                    participant = new_pair)
            registration.save()

            i+=2
            # solo[-1] is not matched with anyone

    def __str__(self):
        return "Solo %s registered for %s" % (self.player, self.tournament)

class Pool(models.Model):
    """Defines a pool of players trying to qualify for the
    knock-off tournament.
    """
    tournament = models.ForeignKey('Tournament')
    number = models.IntegerField(default=0, blank=True)
    winner = models.ForeignKey('players.Pair', null=True, blank=True)

    def compute_winner(self):
        pass #TODO

    def create_matches(self):
        parts = [pp.participant for pp in \
                PoolParticipant.objects.filter(pool=self)]
        print(len(parts))
        for i in range(len(parts)):
            for j in range(i+1, len(parts)):
                match = Match()
                match.team1 = parts[i]
                match.team2 = parts[j]
                match.save()
                pm = PoolMatch()
                pm.pool, pm.match = self, match
                pm.save()

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
