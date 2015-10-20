from django.conf.urls import patterns, url

urlpatterns = patterns('tournament.views',
    url(r'^all$', 'all'),
    url(r'^detail$', 'tournament'),
    url(r'^(\d+)/pool/(\d+)$', 'pool')
)
