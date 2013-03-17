from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, UpdateView
from eece496.models import Session, Student

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(
            queryset=Session.objects.all(),
            context_object_name='session_list',
            template_name='eece496/index.html')),
    url(r'^(?P<pk>\d+)/$',
        UpdateView.as_view(
            model=Session,
            template_name='eece496/detail.html',
            success_url='/eece496')),
)
