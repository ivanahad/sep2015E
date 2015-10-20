from django.db import models

class User(models.Model):
    """This class contains the recorded data on a user.
    """
    firstname = models.CharField(max_length=128, blank=True)
    lastname = models.CharField(max_length=128, blank=True)
    address = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64, blank=True)
    country = models.CharField(max_length=64, blank=True)
    zipcode = models.IntegerField(default=0, blank=True)
    email = models.EmailField(max_length=128, blank=True)
    phone = models.CharField(max_length=32, blank=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.lastname + " " + self.firstname

class Pair(models.Model):
    """This class contains a pair of users registered for a tournament.
    One pair must only participate in one tournament, and a new pair
    must be created for a new tournament.
    We also record the average level between the two players for matchup purposes.
    """
    player1 = models.ForeignKey(User, related_name='player1')
    player2 = models.ForeignKey(User, related_name='player2')
    average = models.IntegerField(default=0)
    season = models.CharField(max_length=32);

    def __str__(self):              # __unicode__ on Python 2
        return self.player1.lastname + " " + self.player2.lastname

PAYMENT_METHODS = (("Cash","Cash"), ("Visa","Visa"), \
        ("Bancontact","Bancontact"), ("MasterCard","MasterCard"), \
        ("Paypal","Paypal"))

class UserRegistration(models.Model):
    """This class contains the data on a single registration for one user.
    For a given event (identified by year), we record the activities desired,
    the payment method used and if the payment has been done.
    """
    user = models.ForeignKey(User)
    season = models.CharField(max_length=32);
    payment_method = models.CharField(choices=PAYMENT_METHODS, max_length=64, \
            default=PAYMENT_METHODS[0])
    payment_done = models.BooleanField(default=False)
    bbq = models.BooleanField(default=False, blank=True)
    activities = models.TextField(max_length=2048, blank=True)
    comment = models.TextField(max_length=2048, default="", blank=True)
    level = models.CharField(max_length=8, blank=True)

    def __str__(self):
        return "Registration of %s for season %s" % (self.user, self.season)
