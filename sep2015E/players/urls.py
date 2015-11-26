from django.conf.urls import patterns, url

urlpatterns = patterns('players.views',
    url(r'^register$', 'register'),
<<<<<<< HEAD
    url(r'^fregister', 'filled_registration'),
=======
    url(r'^payement$', 'payement'),
    url(r'^fregister$', 'filled_registration'),
>>>>>>> origin/master
    url(r'^unregister$', 'unregister'),
    url(r'^unregister_confirm$', 'unregister_confirm'),
)
