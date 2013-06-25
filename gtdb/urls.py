# Urls for app 'gtdb'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('gtdb.views',
    # Examples:
    url(r'^$', 'index', name='index'),
    url(r'^news/$', 'news_modify', name='news_new'),
    url(r'^news/(?P<news_id>\d+)/edit/$', 'news_modify', name='news_modify'),
    url(r'^news/(?P<news_id>\d+)/$', 'news', name='news'),
    url(r'^games/$', 'games', name='games'),
    url(r'^games/(?P<game_id>\d+)/$', 'game', name='game'),
    url(r'^company/$', 'companies', name='companies'),
    url(r'^company/(?P<comp_id>\d+)/$', 'company', name='company'),
)
