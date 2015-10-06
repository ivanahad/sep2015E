from django.db import models

class Staff(models.Model):
    """This class contains the record on a staff member."""
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    zipcode = models.IntegerField(default=0)
    email = models.EmailField(max_length=128)
    phone = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    def __str__(self):              # __unicode__ on Python 2
        return self.lastname + " " + self.firstname
