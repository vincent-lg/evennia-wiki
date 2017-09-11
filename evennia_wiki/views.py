# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

from evennia_wiki.models import Page

def view(request, address):
    """Show the page at this address."""
    if address.startswith("/"):
        address = path[1:]
    page = get_object_or_404(Page, address=address)
    return render(request, "wiki/page.html", context=dict(page=page))
