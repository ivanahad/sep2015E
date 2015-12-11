from django.conf.urls import include, url

prefix = 'staff.views.'

urlpatterns = [
    url(r'^$', prefix+'home'),
    url(r'^players$', prefix+'players'),
    url(r'^courts$', prefix+'courts'),
    url(r'^tournament$', 'tournament.views.all'),
    url(r'^login$', prefix+'login_staff'),
    url(r'^logout$', prefix+'logout_staff'),
    url(r'^home$', prefix+'home'),
    url(r'^search$', prefix+'search'),
    url(r'^profile$', prefix+'edit_profile'),
    url(r'^advanced_search$', prefix+'advanced_search'),
    url(r'^players/(?P<page_id>\d+)$', prefix+'players'),
    url(r'^court/(?P<id_court>\d+)$', prefix+'particular_court'),
    url(r'^players/(?P<page_id>\d+)/(?P<player_id>\d+)$', prefix+'particular_player'),
    url(r'^pairs/(?P<id_pair>\d+)$', prefix+'particular_pair'),
    url(r'^mail_list$', prefix+'mail_list'),
    url(r'^get_file/(?P<id_file>\d+)$', prefix+'send_file'),
    url(r'^tournamentless_pairs/(?P<page_id>\d+)$', prefix+'tournamentless_pairs'),
    url(r'^pairless_players/(?P<page_id>\d+)$', prefix+'pairless_players'),
]
