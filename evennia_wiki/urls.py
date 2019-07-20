# URL patterns for the wiki app

from django.conf.urls import url
from evennia_wiki import views

app_name = 'wiki'

urlpatterns = [
    url(r'^_edit/(.*)$', views.edit, name="edit"),
    url(r'(^[^_].*|^)$', views.view, name="page"),
    url(r'^$', views.view, name="index"),
]
