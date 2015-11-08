from django.db import models
from django.conf import settings

import string


class User(models.Model):
    """This class contains the recorded data on a player.
    """

    def _phone_validator(value):
        for c in value:
            if c in string.ascii_letters:
                raise ValidationError("Phone number %s should not contain letters" % value)

    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    zipcode = models.IntegerField(default=0)
    email = models.EmailField(max_length=128, unique=True)
    phone = models.CharField(max_length=32, )#validators=[_phone_validator]) TODO

    def __str__(self):              # __unicode__ on Python 2
        return self.lastname + " " + self.firstname

    def get_level(self, season):
        reg = UserRegistration.objects.filter(user = self).filter(season = season)
        return reg.first().level


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

    def __str__(self):              # __unicode__ on Python 2
        return self.player1.lastname + " " + self.player2.lastname

    def create_pair(p1, p2):
        """Automatically create a pair from two players for the current season.
        """
        season = settings.CURRENT_SEASON
        new_pair = Pair(player1 = p1, player2 = p2, \
                average = ( p1.get_level(season) + p2.get_level(season) ) / 2, \
                season = season)
        new_pair.save()
        return new_pair


# list of available payment methods
PAYMENT_METHODS = (("Cash","Cash"), ("Visa","Visa"), \
        ("Bancontact","Bancontact"), ("MasterCard","MasterCard"), \
        ("Paypal","Paypal"))

class UserRegistration(models.Model):
    """This class contains the data on a single registration for one user.
    For a given event (identified by year), we record the activities desired,
    the payment method used and if the payment has been done.

    We also store the level, which must be expressed according to NTRP rating
        (http://www.matchmakertennis.com/public/ntrp.html)
    """
    user = models.ForeignKey(User)
    season = models.CharField(max_length=32);
    payment_method = models.CharField(choices=PAYMENT_METHODS, max_length=64, \
            default=PAYMENT_METHODS[0])
    payment_done = models.BooleanField(default=False)
    bbq = models.BooleanField(default=False)
    activities = models.TextField(max_length=2048, blank=True)
    comment = models.TextField(max_length=2048, default="", blank=True)
    level = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return "Registration of %s for season %s" % (self.user, self.season)
