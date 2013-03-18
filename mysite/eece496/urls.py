from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, UpdateView
from eece496.models import Session, Student

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(
            queryset=Session.objects.all(),
            context_object_name='session_list',
            template_name='eece496/index.html')),
    url(r'^(?P<session_id>\d+)/$', 'eece496.views.session'),
)
