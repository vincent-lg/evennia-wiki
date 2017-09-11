# URL patterns for the wiki app

from django.conf.urls import url
from evennia_wiki import views

urlpatterns = [
    url(r'(.*)$', views.view, name="page")
]
