from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template',
        {'template': 'eece496/index.html'}),
    url(r'^polls/', include('polls.urls')),
    url(r'^eece496/', include('eece496.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/', 'django.contrib.auth.views.login',
        {'template_name': 'eece496/login.html'}),
    url(r'^accounts/logout/', 'django.contrib.auth.views.logout',
        {'template_name': 'eece496/logout.html'}),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change',
        {'template_name': 'eece496/password_change_form.html'}),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done',
        {'template_name': 'eece496/password_change_done.html'}),
)
