from django.db import models

class User(models.Model):
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    zipcode = models.IntegerField(default=0)
    email = models.CharField(max_length=128)
    level = models.CharField(max_length=8)
    def __str__(self):              # __unicode__ on Python 2
        return self.lastname + " " + self.firstname
    
class Pair(models.Model):
    player1 = models.ForeignKey(User, related_name='player1')
    player2 = models.ForeignKey(User, related_name='player2')
    average = models.IntegerField(default=0)
    def __str__(self):              # __unicode__ on Python 2
        return self.player1.lastname + " " + self.player2.lastname