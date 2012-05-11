from django.conf.urls.defaults import *
from scrapper.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()
from django.conf import settings

urlpatterns = patterns('',
    # Example:
    # (r'^tweetscrapper/', include('tweetscrapper.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
                       url(r'^twitter/', include('twitter_users.urls')),
			(r'^$', home),                       
			(r'^index/', index),
                       	(r'^scrap/', scrap),
                       	(r'^getpdf/', getpdf),
                       (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),

                       
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',  
         {'document_root':     settings.MEDIA_ROOT}),
    )
