from django.conf.urls import include, url

prefix = 'staff.views.'

urlpatterns = [
    url(r'^home$', prefix+'home'),
    url(r'^courts$', prefix+'courts'),
    url(r'^players$', prefix+'players'),
]
