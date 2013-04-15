from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'eece496.views.past'),
    url(r'^today/$', 'eece496.views.today'),
    url(r'^(?P<cogs_id>\d+)/$', 'eece496.views.sessions'),
    url(r'^(?P<cogs_id>\d+)/(?P<session_id>\d+)/$', 'eece496.views.evaluations'),
    url(r'^(?P<cogs_id>\d+)/(?P<session_id>\d+)/(?P<evaluation_id>\d+)/$',
        'eece496.views.attendance',
        name='attendance_form'),
    # Temporary view to run a parsing script to update the database
    url(r'^update/$', 'eece496.views.update'),
)
