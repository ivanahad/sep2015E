from django.conf.urls import patterns, url

urlpatterns = patterns('tournament.views',
    url(r'^all$', 'all'),
    url(r'^detail/(?P<id_>[0-9]+)$', 'tournament'),
    url(r'^detailStaff/(?P<id_>[0-9]+)$', 'tournamentStaff'),
    url(r'^(?P<id_tournament>\d+)/pool/(?P<id_pool>\d+)$', 'pool'),
    url(r'^pool/save/(?P<id_tournament>\d+)/(?P<id_pool>\d+)/(?P<id_match>\d+)$', 'save_match_changes'),
    url(r'^pools/modify/(?P<id_tournament>\d+)/(?P<id_page>\d+)/(?P<id_pool>\d+)$', 'modify_pools'),
    url(r'^(?P<id_tournament>\d+)/(?P<id_page>\d+)/pool/(?P<id_pool>\d+)/remove/(?P<id_pair>\d+)$', 'remove_player_from_pool'),
    url(r'^(?P<id_tournament>\d+)/(?P<id_page>\d+)/pool/(?P<id_pool>\d+)/add/(?P<id_pair>\d+)$', 'add_player_to_pool'),
    url(r'^assign_pairs_automatic/(?P<id_tournament>\d+)$', 'assign_pairs_for_solo_automatic'),
)
