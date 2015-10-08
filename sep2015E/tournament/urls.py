from django.conf.urls import patterns, url

urlpatterns = patterns('tournament.views',
    url(r'^launch$', 'launch')
)
