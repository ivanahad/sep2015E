from django.conf.urls import patterns, url

urlpatterns = patterns('tournament.views',
    url(r'^all$', 'all'),
    url(r'^detail/(?P<id_>[0-9]+)$', 'tournament'),
    url(r'^(\d+)/pool/(\d+)$', 'pool')
)
