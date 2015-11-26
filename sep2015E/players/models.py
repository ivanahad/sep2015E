from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.conf import settings

import string


class User(models.Model):
    """This class contains the recorded data on a player.
    """

    def _phone_validator(value):
        digits_count = 0
        for c in value:
            if c in string.ascii_letters:
                raise ValidationError("Phone number %s should not contain letters" % value)
            elif c in string.digits:
                digits_count += 1
        if digits_count < 9:
            raise ValidationError("Phone number %s should contain at least 9 digits" % value)

    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    gender = models.CharField(max_length=1, choices=(("M", "Homme"), ("F", "Femme")))
    birthdate = models.DateField()
    address_street = models.CharField(max_length=128)
    address_number = models.CharField(max_length=8)
    address_box = models.CharField(max_length=8, null=True, blank=True)
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    zipcode = models.IntegerField()
    email = models.EmailField(max_length=128, unique=True)
    phone = models.CharField(max_length=32, validators=[_phone_validator])

    def __str__(self):              # __unicode__ on Python 2
        return self.lastname + " " + self.firstname

    def __hash__(self):
        return hash("" + self.email + self.address_street + \
                self.address_number + self.address_box + str(self.birthdate) + \
                self.firstname + self.lastname + settings.HASHKEY) % 100000000

    def get_level(self, season):
        reg = UserRegistration.objects.filter(user = self).filter(season = season)
        return reg.first().level


# list of available payment methods
PAYMENT_METHODS = (("Cash","Cash"), ("Visa","Visa"), \
        ("Bancontact","Bancontact"), ("MasterCard","MasterCard"), \
        ("Paypal","Paypal"))


class Pair(models.Model):
    """This class contains a pair of users registered for a tournament.
    One pair must only participate in one tournament, and a new pair
    must be created for a new tournament.
    We also record the average level between the two players for matchup purposes.
    """
    player1 = models.ForeignKey(User, related_name='player1')
    player2 = models.ForeignKey(User, related_name='player2')
    average = models.DecimalField(max_digits=2, decimal_places=1)
    season = models.CharField(max_length=32);

    # registration details
    payment_method = models.CharField(choices=PAYMENT_METHODS, max_length=64, \
            default=PAYMENT_METHODS[0])
    payment_done = models.BooleanField(default=False)
    comment = models.TextField(max_length=2048, default="", blank=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.player1.lastname + " " + self.player2.lastname


class UserRegistration(models.Model):
    """This class contains the data on a single registration for one user.
    For a given event (identified by year), we record the activities desired,
    the payment method used and if the payment has been done.

    We also store the level, which must be expressed according to NTRP rating
        (http://www.matchmakertennis.com/public/ntrp.html)
    """
    LEVEL_CHOICES = (
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
    )
    user = models.ForeignKey(User)
    season = models.CharField(max_length=32);
    bbq = models.BooleanField(default=False)
    level = models.CharField(max_length=32, choices=LEVEL_CHOICES);

    def __str__(self):
        return "Registration of %s for season %s" % (self.user, self.season)
