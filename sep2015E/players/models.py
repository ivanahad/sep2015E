from django.db import models

class User(models.Model):
    """This class contains the recorded data on a user.
    """
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    zipcode = models.IntegerField(default=0)
    email = models.EmailField(max_length=128)
    phone = models.CharField(max_length=32)
    level = models.CharField(max_length=8)

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

    def __str__(self):              # __unicode__ on Python 2
        return self.player1.lastname + " " + self.player2.lastname

class UserRegistration(models.Model):
    """This class contains the data on a single registration for one user.
    For a given event (identified by year), we record the activities desired,
    the payment method used and if the payment has been done.
    """
    user = models.ForeignKey(User)
    year = models.IntegerField(default=2015)
    payment_method = models.CharField(max_length=64)
    payment_done = models.BooleanField(default=False)
    activities = models.TextField()
