"""sep2015E URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from home import views

urlpatterns = [
    url(r'^$', 'home.views.index'),
    url(r'^sponsors', 'home.views.sponsors'),
    url(r'^contact', 'home.views.contact'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^wiki/', include('waliki.urls')),
    url(r'^players/', include('players.urls')),
    url(r'^courts/', include('courts.urls')),
    url(r'^courts/', 'courts.views.byowner'),
    url(r'^staff/', include('staff.urls')),
    url(r'^tournament/', include('tournament.urls')),
]
