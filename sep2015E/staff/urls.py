from django.conf.urls import include, url

prefix = 'staff.views.'

urlpatterns = [
    url(r'^home$', prefix+'home'),
]
