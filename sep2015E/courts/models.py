from django.db import models

import string

class Court(models.Model):
    """This class defines a tennis court.
    It also includes informations such as how the court can be used,
    what his type is and who is the owner."""
    GROUND_TYPES=(
        ('brique', 'brique'),
        ('beton', 'béton'),
        ('synthetique', 'synthétique'),
        ('terre battue', 'terre battue'),
        ('quick', 'quick'),
        ('autres', 'autres')
    )
    def _phone_validator(value):
        """ Check if the phone entered by the player is correct """
        digits_count = 0
        for c in value:
            if c in string.ascii_letters:
                raise ValidationError("Phone number %s should not contain letters" % value)
            elif c in string.digits:
                digits_count += 1
        if digits_count < 9:
            raise ValidationError("Phone number %s should contain at least 9 digits" % value)

    owner = models.CharField(max_length=128)
    owner_address_street = models.CharField(max_length=128)
    owner_address_number = models.CharField(max_length=8)
    owner_address_box = models.CharField(max_length=8, null=True, blank=True)
    city = models.CharField(max_length=64)
    zipcode = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=32, validators=[_phone_validator])

    address_street = models.CharField(max_length=128)
    address_number = models.CharField(max_length=8)
    address_box = models.CharField(max_length=8, null=True, blank=True)
    ground = models.CharField(max_length=128, choices=GROUND_TYPES, default='autres')
    cover = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True)
    comment_access = models.TextField(default="", blank=True)
    comment_desiderata = models.TextField(default="", blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):              # __unicode__ on Python 2
        """ to string method """
        return "%s %s %s" % (self.owner, self.address_street, self.address_number)
