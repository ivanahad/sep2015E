from django.conf.urls import include, url

prefix = 'staff.views.'

urlpatterns = [
    url(r'^login$', prefix+'login_staff'),
    url(r'^logout$', prefix+'logout_staff'),
    url(r'^home$', prefix+'home'),
    url(r'^courts$', prefix+'courts'),
    url(r'^search$', prefix+'search'),
    url(r'^players/(?P<page_id>\d+)$', prefix+'players'),
    url(r'^players/(?P<page_id>\d+)/(?P<player_id>\d+)$', prefix+'particular_player'),
    url(r'^pairs/(?P<id_pair>\d+)$', prefix+'particular_pair'),
    url(r'^mail_list$', prefix+'mail_list'),
    url(r'^get_file/(?P<id_file>\d+)$', prefix+'send_file'),
    url(r'^tournamentless_pairs/(?P<page_id>\d+)$', prefix+'tournamentless_pairs'),
]
