from django.db import models
from io import BytesIO
import time
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, Frame, PageTemplate, NextPageTemplate, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
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
        doc = SimpleDocTemplate("pools.pdf", rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18, showBoundary=1)
        doc.pagesize=landscape(A4)
        Story=[]

        file_path="file_path"
        date = time.ctime()
        header_title="CDL - tableaux de poules"
        number_pool="10"
        field="Jc et Nath \n3080 Tervuren"
        tournament="Double Mixte - Juniors - JUN"

        #frames
        frameTable = Frame(doc.leftMargin, doc.height*0.20,
                    doc.height-doc.rightMargin , 400,
                    leftPadding=0, rightPadding=0, id='normal')

        def footer_header(canvas,doc):
            """Footer and header description"""
            canvas.saveState()
            canvas.setFont('Times-Roman',12)

            #Header
            header_y=doc.height + 72
            canvas.drawString(20, header_y, date)
            canvas.drawString(doc.width/2, header_y, header_title)
            canvas.drawString(doc.leftMargin, header_y-20, "Numéro:")
            canvas.drawString(doc.leftMargin+100, header_y-20, "Terrain:")
            canvas.drawString(doc.leftMargin+5, header_y-45, number_pool)
            canvas.drawString(doc.leftMargin+105, header_y-45, field)
            canvas.drawString(doc.leftMargin+5, header_y-70, tournament)

            #Footer
            footer_y=10
            canvas.drawString(25, footer_y, file_path)
            canvas.drawString(doc.width , footer_y, "page %d" % doc.page)
            canvas.restoreState()

        #Table score

        pools = Pool.objects.filter(tournament=self);
        templates=[]
        for pool in pools:
            Story.append(Spacer(1, 48))
            Story.append(self.pdf_pool(pool))
            Story.append(NextPageTemplate(str(pool)))
            Story.append(PageBreak())
            templates.append(PageTemplate(id=str(pool),frames=frameTable,onPage=footer_header))

        doc.addPageTemplates(templates)

        doc.build(Story)


    def pdf_pool(self, pool):
        participants = PoolParticipant.objects.filter(pool=pool) #List of participants
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        #create header for table
        header_table=['Joueurs']
        for i in range(0,len(participants)):
            header_table.append(i+1)
        header_table.append('V/Pts')
        #Add the rows
        data = [header_table]
        for p in participants:
            ptext=Paragraph(str(p), styles["Normal"])
            data.append([ptext])
        t = Table(data)
        t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                ('ALIGN',(0,0),(-1,-1),'CENTER'),]))
        return t


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
