from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    #Basic Pages
    url(r'^$', info_page, {"page":"GPS"}),
    url(r'^welcome/?$', info_page, {"page":"welcome"}),

    url(r'^explore/?$', info_page, {"page":"explore"}),
    url(r'^GPS/?$', info_page, {"page":"GPS"}),
    url(r'^about/?$', info_page, {"page":"about"}),
    url(r'^graph/?$',info_page, {"page":"graph"}),
    url(r'^career/?$', career),
    #Node Views
    url(r'^node/?$', node),
    url(r'^random/?$', random_node),

    #Authentication
    url(r'^login/?$', login),
    url(r'^logout/?$', logout_view),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^done/?$', info_page, {"page":"explore"}),

    #Model Construction/Editing
    url(r'^node_form/?$', node_form),
    url(r'^career_form/?$', career_form),
    url(r'^edge_form/?$', edge_form),
    url(r'^edit_node/$', edit_node),

    #User-based perspectives.
    url(r'^my_nodes/?$', user_nodes),
    url(r'^my_careers/?$', user_careers),

    #AJAX URLs
    url(r'^get_node_names/$', get_node_names),
    url(r'^get_edges/$', get_edge_pairs),
    url(r'^get_career_names/$', get_career_names),
    url(r'^vote/$', vote),
)
