from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^polls/', include('polls.urls')),
    url(r'^eece496/', include('eece496.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
