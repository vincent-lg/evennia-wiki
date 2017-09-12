# URL patterns for the wiki app

from django.conf.urls import url
from evennia_wiki import views

urlpatterns = [
    url(r'^_edit/(.*)$', views.edit, name="page"),
    url(r'(^[^_].*|^)$', views.view, name="page"),
]
