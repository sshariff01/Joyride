from django.conf.urls import patterns, url

from givers import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)