from django.conf.urls import patterns, url

urlpatterns = patterns('players.views',
    url(r'^register$', 'register'),
    url(r'^payement/(?P<id_user1>\d+)/(?P<id_user2>-?\d+)/(?P<id_registration1>\d+)/(?P<id_registration2>-?\d+)/(?P<id_pair>-?\d+)$', 'payement'),
    url(r'^fregister$', 'filled_registration'),
    url(r'^unregister$', 'unregister'),
    url(r'^unregister_confirm$', 'unregister_confirm'),
)
