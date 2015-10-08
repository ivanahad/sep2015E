from django.db import models

class Court(models.Model):
    """This class defines a tennis court.
    It also includes informations such as how the court can be used,
    what his type is and who is the owner."""
    owner = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    zipcode = models.IntegerField(default=0)
    email = models.EmailField()
    phone = models.CharField(max_length=32)
    ground = models.CharField(max_length=128)
    cover = models.BooleanField(default=False)
    image = models.ImageField(blank=True)
    comment_access = models.TextField(default="")
    comment_desiderata = models.TextField(default="")
    available = models.BooleanField(default=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.owner + " " + self.address
