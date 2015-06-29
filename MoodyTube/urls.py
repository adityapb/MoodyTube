from django.conf.urls import patterns, include, url
from django.contrib import admin
from MoodyTube.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MoodyTube.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', PlayMusic),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^register/$', register_page),
    url(r'^logout/$', logout_page),
)
