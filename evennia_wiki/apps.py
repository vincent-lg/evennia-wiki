# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from evennia_wiki.models import Page, Revision

class EvenniaWikiConfig(AppConfig):
    name = 'evennia_wiki'
    verbose_name = 'A wiki for Evennia'
    label = 'evennia_wiki'
