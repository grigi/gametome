# Urls for app 'gtdb'
from django.conf.urls import patterns, url

urlpatterns = patterns('gallery.views',
    url(
        '^(?P<album_slug>[-\w]+)/(?P<pk>[0-9]+)/(?P<slug>[-\w]+)/$',
        'picture_detail',
        name='galeria-picture'
    ),
    url(
        '^(?P<slug>[-\w]+)/$',
        'album_detail',
        name='galeria-album'
    ),
    url('^$', 'album_list', name='galeria-album-list'),
)

