from django.core.management.base import BaseCommand
from players.models import User
import random
import linecache
class Command(BaseCommand):
    args = '<>'
    help = 'Populate the database'

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

    def _create_users(self):
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

    def handle(self, *args, **options):
        self._create_users()
