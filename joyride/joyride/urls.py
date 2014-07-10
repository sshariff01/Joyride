from django.conf.urls import patterns, include, url

from django.contrib import admin

from givers import views as giversviews

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'joyride.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', giversviews.index, name='index'),
    url(r'^index/', giversviews.index, name='index'),
    url(r'^search/', giversviews.search, name='search'),
    url(r'^profile/', giversviews.profile, name='profile'),
    url(r'^post_user/', giversviews.post_user, name='post_user'),

    url(r'^admin/', include(admin.site.urls)),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()