from django.test import TestCase, Client
from players.models import User, Pair
from tournament.models import Tournament
from django.conf import settings

class VisitorPosts(TestCase):
    def test_tournamentSubscriptionSolo(self):
        print("*** Test if a visitor can register to a Tournament***")
        c = Client()
        c.firstname = "Geoffroy"
        c.lastname = "Husson"
        c.gender = "M"
        c.birthdate = "12/02/1993"
        c.address_street = "Avenue de l'université"
        c.address_number = "1"
        c.address_box = ""
        c.city = "Bruxelles"
        c.country = "Belgique"
        c.zipcode = "1348"
        c.email = "sep2015e@yopmail.com"
        c.phone = "0478841254"
        response = c.post('http://127.0.0.1:8000/players/register')
        self.assertEqual(response.status_code, 200, \
            "Error: Test players register post return " + \
             str(response.status_code))



