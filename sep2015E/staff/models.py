from django.db import models
from django.contrib.auth.models import User

class Staff(models.Model):
    """This class contains the record on a staff member. Use the user
        model defined by django."""
    user = models.OneToOneField(User)
    address = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    zipcode = models.IntegerField(default=0)
    phone = models.CharField(max_length=32)

    def __str__(self):              # __unicode__ on Python 2
        return str(self.user)

class Messages(models.Model):
    """ This class contains the messages sent between the staff"""
    author = models.CharField(max_length=128)
    destinator = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    message = models.TextField(default="", blank=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.title + " " + self.message

class Files(models.Model):
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(User)
    f = models.FileField(upload_to="files/")

    def __str__(self):
        return str(self.name)
