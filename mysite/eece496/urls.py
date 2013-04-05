from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth.decorators import login_required
from eece496.models import Session, Attendance, Evaluation

urlpatterns = patterns('',
    url(r'^$', 'eece496.views.sessions'),
    url(r'^upload/$', 'eece496.views.upload'),
    url(r'^(?P<session_id>\d+)/$', 'eece496.views.evaluations'),
    url(r'^(?P<session_id>\d+)/(?P<evaluation_id>\d+)/$',
        'eece496.views.attendance',
        name='attendance_form'),
)
