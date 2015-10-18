from django.contrib import admin

from .models import User, Pair, UserRegistration

admin.site.register(User)
admin.site.register(Pair)
admin.site.register(UserRegistration)
