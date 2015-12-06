from django.test import TestCase, Client
from tournament.models import Tournament
from django.conf import settings

#THIS SCRIPT IS FOR TESTING IF THE LINKS REDIRECT TO THE RIGHT TEMPLATES
#FOR THE VISITORS PAGES

class VisitorsPagesAccessCase(TestCase):
    def test_pages(self):
        print("*** Test for accesses of visitors pages ***")
        print("--No tournament open")
        c = Client()
        #Test home page
        url = '/'
        response = c.get(url)
        self.assertEqual(response.status_code, 200, \
            "Error: Test home page return " + str(response.status_code))
        print("\nTemplates for " + url)
        templates = response.templates
        for template in templates:
            print(template.name)
        #Test players register page
        url = '/players/register'
        response = c.get(url)
        self.assertEqual(response.status_code, 200, \
            "Error: Test players register page return " + \
             str(response.status_code))
        print("\nTemplates for " + url)
        templates = response.templates
        for template in templates:
            print(template.name)
        #Test courts register page
        url = '/courts/register'
        response = c.get(url)
        self.assertEqual(response.status_code, 200, \
            "Error: Test courts register page return " + \
            str(response.status_code))
        print("\nTemplates for " + url)
        templates = response.templates
        for template in templates:
            print(template.name)
        #Test sponsors page
        url = '/sponsors'
        response = c.get(url)
        self.assertEqual(response.status_code, 200, \
            "Error: Test sponsors page return " + \
            str(response.status_code))
        print("\nTemplates for " + url)
        templates = response.templates
        for template in templates:
            print(template.name)
        #Test contact page
        url = '/contact'
        response = c.get(url)
        self.assertEqual(response.status_code, 200, \
            "Error: Test contact page return " + \
            str(response.status_code))
        print("\nTemplates for " + url)
        templates = response.templates
        for template in templates:
            print(template.name)

    def test_pages_open_tournament(self):
        name = "Tournament test"
        category = "cadets"
        pool_size = 5
        mixte = 'M'
        season = settings.CURRENT_SEASON
        tournament = Tournament(name=name, category=category, \
        pool_size=pool_size, mixte=mixte, season=season)
        tournament.save()

        print("\n\n--Tournament open")
        c = Client()
        #Test home page
        url = '/'
        response = c.get(url)
        self.assertEqual(response.status_code, 200, \
            "Error: Test home page return " + str(response.status_code))
        print("\nTemplates for " + url)
        templates = response.templates
        for template in templates:
            print(template.name)
        #Test players register page
        url = '/players/register'
        response = c.get(url)
        self.assertEqual(response.status_code, 200, \
            "Error: Test players register page return " + \
             str(response.status_code))
        print("\nTemplates for " + url)
        templates = response.templates
        for template in templates:
            print(template.name)
        #Test courts register page
        url = '/courts/register'
        response = c.get(url)
        self.assertEqual(response.status_code, 200, \
            "Error: Test courts register page return " + \
            str(response.status_code))
        print("\nTemplates for " + url)
        templates = response.templates
        for template in templates:
            print(template.name)
        #Test sponsors page
        url = '/sponsors'
        response = c.get(url)
        self.assertEqual(response.status_code, 200, \
            "Error: Test sponsors page return " + \
            str(response.status_code))
        print("\nTemplates for " + url)
        templates = response.templates
        for template in templates:
            print(template.name)
        #Test contact page
        url = '/contact'
        response = c.get(url)
        self.assertEqual(response.status_code, 200, \
            "Error: Test contact page return " + \
            str(response.status_code))
        print("\nTemplates for " + url)
        templates = response.templates
        for template in templates:
            print(template.name)
