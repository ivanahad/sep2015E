from django.conf.urls import patterns, url

urlpatterns = patterns('tournament.views',
    url(r'^all$', 'all'),
    url(r'^allUser$', 'allUser'),
    url(r'^detail/(?P<id_>[0-9]+)$', 'tournament'),
    url(r'^(?P<id_tournament>\d+)/pool/(?P<id_pool>\d+)$', 'pool'),
    url(r'^pool/save/(?P<id_tournament>\d+)/(?P<id_pool>\d+)/(?P<id_match>\d+)$', 'save_match_changes'),
)
