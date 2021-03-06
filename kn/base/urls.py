from django.conf.urls.defaults import *

import django.views.generic.simple
import django.views.generic as generic
import django.contrib.auth.views

urlpatterns = patterns('',
    url(r'^styles/bare/$',
        generic.simple.direct_to_template,
        {'template':'base/bare.css',
         'mimetype':'text/css'}, name='style-bare'),
    url(r'^styles/base/$',
        generic.simple.direct_to_template,
        {'template':'base/base.css',
         'mimetype':'text/css'}, name='style-base'),
)

# vim: et:sta:bs=2:sw=4:
