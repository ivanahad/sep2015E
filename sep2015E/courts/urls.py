from django.conf.urls import patterns, url

urlpatterns = patterns('courts.views',
    url(r'^register$', 'register'),
    url(r'^(?P<param>.*)/byowner', 'byowner'),
)
