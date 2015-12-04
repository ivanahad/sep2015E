from django.core.management.base import BaseCommand
from django.conf import settings
from players.models import User, UserRegistration, Pair
from courts.models import Court
import random
import linecache
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
        year = str(random.randint(1970, 2005))
        month = str(random.randint(1, 12))
        day = str(random.randint(1, 28))
        return year + "-" + month + "-" + day

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

    def _create_pair(self, player1, player2):
        average = 1
        season = settings.CURRENT_SEASON

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

    def handle(self, *args, **options):
        user = self._create_user()
        user_registration = self._create_user_registration(user)
        user_bis = self._create_user()
        user_bis_registration = self._create_user_registration(user)
        pair = self._create_pair(user, user_bis)
        court = self._create_court()
        print(court)
