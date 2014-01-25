from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    # Examples:
    url(r'^$', home),
    url(r'^index/?$', home),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login/$', login),
    url(r'^done/$', home),
    url(r'^node/?$', node),
    url(r'^node_form/?$', node_form),
    url(r'^my_nodes/?$', user_nodes),
    url('', include('social.apps.django_app.urls', namespace='social')),
)
