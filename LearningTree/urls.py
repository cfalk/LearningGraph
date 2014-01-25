from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    #Basic Pages
    url(r'^$', info_page, {"page":"welcome"}),
    url(r'^welcome/?$', info_page, {"page":"welcome"}),

    url(r'^explore/?$', info_page, {"page":"explore"}),
    url(r'^GPS/?$', info_page, {"page":"GPS"}),
    url(r'^about/?$', info_page, {"page":"about"}),
    url(r'^graph/?$',info_page, {"page":"graph"}),

    #Node Views
    url(r'^node/?$', node),
    url(r'^random/?$', random),

    #Authentication
    url(r'^login/?$', login),
    url(r'^logout/?$', logout_view),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^done/?$', info_page, {"page":"explore"}),

    #Model Construction/Editing
    url(r'^node_form/?$', node_form),
    url(r'^career_form/?$', career_form),

    #User-based perspectives.
    url(r'^my_nodes/?$', user_nodes),

    #AJAX URLs
    url(r'^get_node_names/$', get_node_names),

)
