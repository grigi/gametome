from os.path import dirname,normpath,abspath,join
from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.conf import settings
from gametome.views import profile_view
from django.conf.urls.static import static

# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Admin documentation
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Admin panel
    url(r'^admin/logout/$', 'allauth.account.views.logout', name='admin:logout'),  
    url(r'^admin/', include(admin.site.urls)),
    # AllAuth & Profile
    url(r'^accounts/profile/$', profile_view, name='profile'),
    url(r'^accounts/', include('allauth.urls')),
    # Haystack - Search
    (r'^search/', include('haystack.urls')),
    # PyBBM
    (r'^forum/', include('pybb.urls', namespace='pybb')),
    # Gallery
    (r'^gallery/', include('gallery.urls')),
    
    # GTDB - fallthrough
    url(r'^', include('gtdb.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files only if DEBUG=True
# See: https://docs.djangoproject.com/en/dev/howto/static-files/
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    staticroot = normpath(join(settings.PROJECT_ROOT, 'gametome/static'))
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        (r'^favicon\.ico$', 'django.views.static.serve', { 'document_root': staticroot, "path":'favicon.ico' }),
        (r'^robots\.txt$', 'django.views.static.serve', { 'document_root': staticroot, "path":'robots.txt' }),
        (r'^crossdomain\.xml$', 'django.views.static.serve', { 'document_root': staticroot, "path":'crossdomain.xml' }),
    )

