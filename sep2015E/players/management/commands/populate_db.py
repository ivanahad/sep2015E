from django.core.management.base import BaseCommand
from django.conf import settings
from players.models import User, UserRegistration, Pair
from courts.models import Court
from tournament.models import Tournament, TournamentParticipant, SoloParticipant
import random
import linecache
from datetime import datetime
from datetime import date

class Command(BaseCommand):
    args = '<>'
    help = 'Populate the database'

    #CREATE USER
    def random_name_gender(self):
        #Choose the gender
        gender = "M" if random.randint(0,1) == 0 else "F"
        #Choose the firstname based on the gender
        if gender == "M":
            a = 1
            b = int(linecache.getline('static/txt/male.txt', 1))
            firstname = linecache.getline('static/txt/male.txt', random.randint(a, b))
        else:
            a = 1
            b = int(linecache.getline('static/txt/female.txt', 1))
            firstname = linecache.getline('static/txt/female.txt', random.randint(a, b))
        #Choose the lastname
        a = 1
        b = int(linecache.getline('static/txt/names', 1))
        lastname = linecache.getline('static/txt/names', random.randint(a, b))

        return firstname, lastname, gender

    def random_birthdate(self):
        year = random.randint(1970, 2007)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return date(year, month, day)

    def random_address_number(self):
        return str(random.randint(1, 250))

    def random_address_box(self):
        return str(random.randint(1,20))

    def random_zipcode(self):
        return random.randint(1, 2000)

    def random_phone(self):
        phone = ""
        for i in range(0,9):
            phone += str(random.randint(0,9))
        return phone

    def random_city(self):
        CITY_LIST=["Louvain", "Brugges", "Namur", "Ottignies", "Bruxelles", \
                "Gembloux", "Hastre", "Gant", "Anvers", "Liège"]
        a = 0
        b = len(CITY_LIST)-1
        return CITY_LIST[random.randint(a, b)]

    def random_street(self):
        STREET_LIST=["La rue", "Victoire", "Trébuchet", "Horde d'or", \
                "Megal", "Marais"]
        a = 0
        b = len(STREET_LIST)-1
        return STREET_LIST[random.randint(a, b)]

    def _create_user(self):
        firstname, lastname, gender = self.random_name_gender()
        birthdate = self.random_birthdate()
        address_street = self.random_street()
        address_number = self.random_address_number()
        address_box = self.random_address_box()
        city = self.random_city()
        country = "Belgique"
        zipcode = self.random_zipcode()
        email = firstname + "." +lastname + "@test.com"
        phone = self.random_phone()

        while User.objects.filter(email=email).count ==0:
            email = "0" + email

        user = User(firstname=firstname, lastname=lastname, gender=gender, \
                birthdate=birthdate, address_street=address_street, \
                address_number=address_number, address_box=address_box, \
                city=city, country=country, zipcode=zipcode, email=email, \
                phone=phone)
        user.save()

        return user

    #CREATE USER REGISTRATION

    def _create_user_registration(self, user):
        LEVEL_CHOICES = [
                ('-','-'),
                ('C30.5', 'C30.5'),
                ('C30.4', 'C30.4'),
                ('C30.3', 'C30.3'),
                ('C30.2', 'C30.2'),
                ('C30.1', 'C30.1'),
                ('C30', 'C30'),
                ('C15.5', 'C15.5'),
                ('C15.4', 'C15.4'),
                ('C15.3', 'C15.3'),
                ('C15.2', 'C15.2'),
                ('C15.1', 'C15.1'),
                ('C15', 'C15'),
                ('B+4/6', 'B+4/6'),
                ('B+2/6', 'B+2/6'),
                ('B0', 'B0'),
                ('B-2/6', 'B-2/6'),
                ('B-4/6', 'B-4/6'),
                ('B-15', 'B-15'),
                ('B-15.1', 'B-15.1'),
                ('B-15.2', 'B-15.2'),
                ('B-15.4', 'B-15.4'),
                ('A4', 'A4'),
                ('A3', 'A3'),
                ('A2', 'A2'),
                ('A1', 'A1')
            ]

        PAYMENT_METHODS = [("Cash","Cash"), ("Visa","Visa"), \
            ("Bancontact","Bancontact"), ("MasterCard","MasterCard"), \
            ("Paypal","Paypal")]

        season = settings.CURRENT_SEASON
        bbq = random.randint(0,1) == 0
        a = 0
        b = len(LEVEL_CHOICES)-1
        level = LEVEL_CHOICES[random.randint(a, b)][0]
        b = len(PAYMENT_METHODS)-1
        payement_method = PAYMENT_METHODS[random.randint(a, b)][0]
        payement_done = random.randint(0,1) == 0

        user_registration = UserRegistration(user=user, season=season, bbq=bbq, \
                level=level, payement_method=payement_method, \
                payement_done=payement_done)
        user_registration.save()

        return user_registration

    #CREATE PAIR

    def _create_pair(self, player1, player2, same_birthdate=False):
        average = 1
        season = settings.CURRENT_SEASON
        if same_birthdate == True:
            player2.birthdate = player1.birthdate
            player2.save()
        pair = Pair(player1=player1, player2=player2, average=average, \
                season=season)
        pair.save()

        return pair

    #CREATE COURT
    def _create_court(self):
        GROUND_TYPES=[
            ('brique', 'brique'),
            ('beton', 'béton'),
            ('synthetique', 'synthétique'),
            ('terre battue', 'terre battue'),
            ('quick', 'quick'),
            ('autres', 'autres')
        ]

        firstname, lastname, gender = self.random_name_gender()
        owner = firstname + " " + lastname
        owner_address_street = self.random_street()
        owner_address_number = self.random_address_number()
        owner_address_box = self.random_address_box()
        city = self.random_city()
        zipcode = self.random_zipcode()
        email = firstname + "." + lastname + "@owner.com"
        phone = self.random_phone()

        address_street = self.random_street()
        address_number = self.random_address_number()
        address_box = self.random_address_box()
        a = 0
        b = len(GROUND_TYPES)-1
        ground = GROUND_TYPES[random.randint(a,b)][0]
        cover = random.randint(0,1) == 0
        available = random.randint(0,1) == 0

        court = Court(owner=owner, owner_address_street=owner_address_street, \
            owner_address_number=owner_address_number, owner_address_box=owner_address_box, \
            city=city, zipcode=zipcode, email=email, phone=phone, address_street=address_street, \
            address_number=address_number, address_box=address_box, ground=ground, cover=cover,\
            available=available)
        court.save()

        return court

    #CREATE TOURNAMENT
    def _create_tournament(self, category_id, mixte_id):
        CATEGORIES_LIST=[
            ('preminimes', 'pré-minimes'),
            ('minimes', 'minimes'),
            ('cadets', 'cadets'),
            ('scolaires', 'scolaires'),
            ('juniors', 'juniors'),
            ('seniors', 'seniors'),
            ('elites', 'elites'),
            ('familles', 'tournoi des familles')
        ]
        MIXTE_CHOICES=[
            ('M', 'masculin'),
            ('F', 'féminin'),
            ('Mixte', 'mixte')
        ]
        category = CATEGORIES_LIST[category_id][0]
        pool_size = 5
        mixte = MIXTE_CHOICES[mixte_id][0]
        season = settings.CURRENT_SEASON
        name = "Tournoi " + category + " " + mixte
        tournament = Tournament(name=name, category=category, pool_size=pool_size, \
            mixte=mixte, season=season)
        tournament.save()

        return tournament

    #CREATE TOURNAMENT PARTICIPANT

    def assign_tournament_pair(self, pair):
        """ Assign a tournament to a pair based on their genders (if same or different)
            and their birthdate. The category is based on the older player.
            It may happen that some players are not assigned tournaments (don'f fit)."""
        player1 = pair.player1
        player2 = pair.player2

        #Check if mixte
        if player1.gender != player2.gender:
            mixte = "Mixte"
        elif player1.gender == "M":
            mixte = "M"
        else:
            mixte = "F"

        #Assign the category based on birthdate
        current_year = datetime.now().year
        player1_birth_year = player1.birthdate.year
        player2_birth_year = player2.birthdate.year
        smaller_difference = current_year - player1_birth_year
        if current_year - player2_birth_year > current_year - player1_birth_year:
            smaller_difference = current_year - player2_birth_year

        category = "none"
        if smaller_difference <= 10 and smaller_difference >=9:
            category = "preminimes"
        elif smaller_difference <= 12 and smaller_difference >=11:
            category = "minimes"
        elif smaller_difference <= 14 and smaller_difference >=13:
            category = "cadets"
        elif smaller_difference <= 16 and smaller_difference >=15:
            category = "scolaires"
        elif smaller_difference <= 19 and smaller_difference >=17:
            category = "juniors"
        elif smaller_difference <= 40 and smaller_difference >=20:
            category = "seniors"
        elif smaller_difference > 40:
            category = 'elites'

        if current_year - player1_birth_year <= 15:
            if current_year - player2_birth_year >= 25:
                category = "familles"
                mixte = "Mixte"
        elif current_year - player2_birth_year <= 15:
            if current_year - player1_birth_year >= 25:
                category = "familles"
                mixte = "Mixte"

        #Assign a tournament if possible
        exist = (Tournament.objects.filter(category=category, mixte=mixte, \
            season=settings.CURRENT_SEASON).count() != 0)
        if exist:
            return Tournament.objects.get(category=category, mixte=mixte, \
                season=settings.CURRENT_SEASON)

        return None

    def _create_tournament_partipant(self, pair):
        tournament = self.assign_tournament_pair(pair)
        if tournament != None:
            participant = TournamentParticipant(tournament=tournament, \
                participant=pair)
            participant.save()
            return participant
        return None

    #CREATE SOLO PARTICIPANT

    def assign_tournament_solo(self, player):

        #Assign the category based on birthdate
        current_year = datetime.now().year
        player_birth_year = player.birthdate.year
        smaller_difference = current_year - player_birth_year

        if player.gender == "M":
            mixte = "M"
        else:
            mixte = "F"

        category = "none"
        if smaller_difference <= 10 and smaller_difference >=9:
            category = "preminimes"
        elif smaller_difference <= 12 and smaller_difference >=11:
            category = "minimes"
        elif smaller_difference <= 14 and smaller_difference >=13:
            category = "cadets"
        elif smaller_difference <= 16 and smaller_difference >=15:
            category = "scolaires"
        elif smaller_difference <= 19 and smaller_difference >=17:
            category = "juniors"
        elif smaller_difference <= 40 and smaller_difference >=20:
            category = "seniors"
        elif smaller_difference > 40:
            category = 'elites'

        #Assign a tournament if possible
        exist = (Tournament.objects.filter(category=category, mixte=mixte, season=settings.CURRENT_SEASON).count() != 0)
        if exist:
            tournament= Tournament.objects.get(category=category, mixte=mixte, season=settings.CURRENT_SEASON)
            tp = SoloParticipant(player=player, tournament=tournament)
            tp.save()
        else:
            tp = SoloParticipant(player=player)
            tp.save()
        return tp

    def _create_solo_participant(self, player):
        return self.assign_tournament_solo(player)

    def handle(self, *args, **options):
        print("Can take few minutes\n")
        #Create all tournaments possible
        print("Create tournaments\n")
        for i in range(0, 7):
            for j in range(0, 3):
                self._create_tournament(i,j)
        self._create_tournament(7, 2) #Tournoi des familles
        #Create 20 courts
        print("Create courts\n")
        for i in range(0, 20):
            self._create_court()
        #Create 100 pairs
        print("Create pairs\n")
        for i in range(0, 100):
            user = self._create_user()
            user_registration = self._create_user_registration(user)
            user_bis = self._create_user()
            user_bis_registration = self._create_user_registration(user)
            same_birthdate = random.randint(0,4) != 0
            pair = self._create_pair(user, user_bis, same_birthdate=same_birthdate)
            participant = self._create_tournament_partipant(pair)
        #Create 30 solo players
        print("Create solo players\n")
        for i in range(0, 30):
            user_tri = self._create_user()
            user_tri_registration = self._create_user_registration(user_tri)
            solo = self._create_solo_participant(user_tri)
