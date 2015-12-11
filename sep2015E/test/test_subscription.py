from django.test import TestCase, Client
from players.models import User, Pair
from tournament.models import Tournament
from django.conf import settings

class VisitorPosts(TestCase):
    def setUp(self):
        name = "Tournament test"
        category = "cadets"
        pool_size = 5
        mixte = 'M'
        season = settings.CURRENT_SEASON
        tournament = Tournament(name=name, category=category, \
        pool_size=pool_size, mixte=mixte, season=season)
        tournament.save()

    def test_tournamentSubscriptionSolo(self):
        print("*** Test if a visitor can register to a Tournament***")
        print("Post player form to url: /players/register")
        c = Client()
        firstname = "Geoffroy"
        lastname = "Husson"
        gender = "M"
        birthdate = "12/02/1993"
        address_street = "Avenue de l'université"
        address_number = "1"
        address_box = ""
        city = "Bruxelles"
        country = "Belgique"
        zipcode = "1348"
        email = "sep2015e@yopmail.com"
        phone = "0478841254"
        level = "C30.5"
        bbq = True
        response = c.post('/players/register', {'usr1-firstname':firstname,\
            'usr1-lastname':lastname, 'usr1-gender':gender, 'usr1-birthdate':birthdate,\
            'usr1-address_street':address_street, 'usr1-address_number':address_number,\
            'usr1-address_box':address_box, 'usr1-city':city, 'usr1-country':country,\
            'usr1-zipcode':zipcode, 'usr1-email':email, 'usr1-phone':phone, 'reg1-level':level,\
            'reg1-bbq':bbq, 'reg1-payement_done':True, 'reg1-payement_method':"Bancontact", \
            'solo_registration':'Inscription solo', 'usr2-firstname':firstname,\
            'usr2-lastname':lastname, 'usr2-gender':gender, 'usr2-birthdate':birthdate,\
            'usr2-address_street':address_street, 'usr2-address_number':address_number,\
            'usr2-address_box':address_box, 'usr2-city':city, 'usr2-country':country,\
            'usr2-zipcode':zipcode, 'usr2-email':email, 'usr2-phone':phone, 'reg2-level':level,\
            'reg2-payement_done':True, 'reg2-payement_method':"Bancontact", \
            'reg2-bbq':bbq, 'comment':"Null"}, follow=True)
        self.assertEqual(response.status_code, 200, \
            "Error: Test players register post return " + \
             str(response.status_code))
        print("Response templates:")
        templates = response.templates
        for template in templates:
            print("- "+template.name)

        print("Post registration form to url:" + response.request['PATH_INFO'])
        response = c.post(response.request['PATH_INFO'], {'payement_method':"Maestro"})
        self.assertEqual(response.status_code, 200, \
            "Error: Test players register post return " + \
             str(response.status_code))
        print("Response templates:")
        templates = response.templates
        for template in templates:
            print("- "+template.name)

        print("\n")

    def test_courtRegister(self):
        print("*** Test if a visitor can register ta new court***")
        print("Post court form to url: /courts/register")
        c = Client()
        owner_firstname = "Geoffroy"
        owner_lastname = "Husson"
        owner_address_street = "Avenue de l'université"
        owner_address_number = "1"
        owner_address_box = ""
        city = "Bruxelles"
        zipcode = "1348"
        email = "sep2015e@yopmail.com"
        phone = "0478841254"
        address_street = "Avenue du terrain de tennis"
        address_number = "1"
        address_box = ""
        ground = "Brique"
        cover = True
        image = ""
        comment_access = "accessible aux chaises roulantes"
        comment_desiderata = "pas de commentaire"
        available = "Samedi"
        response = c.post('/courts/register', {'owner_firstname':owner_firstname,\
            'owner_lastname':owner_lastname, 'owner_address_street':owner_address_street,\
            'owner_address_number':owner_address_number, 'owner_address_box':owner_address_box,\
            'city':city, 'zipcode':zipcode, 'email':email, 'phone':phone, 'address_street':address_street,\
            'address_number':address_number, 'address_box':address_box, 'ground':ground, 'cover':cover,\
            'image':image, 'comment_access':comment_access, 'comment_desiderata':comment_desiderata,\
            'available':available},follow=True)
        self.assertEqual(response.status_code, 200, \
            "Error: Test court register post return " + \
             str(response.status_code))
        print("Response templates:")
        templates = response.templates
        for template in templates:
            print("- "+template.name)


