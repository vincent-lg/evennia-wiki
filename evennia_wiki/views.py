# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render

from evennia_wiki.forms import PageForm
from evennia_wiki.models import Page

def view(request, address):
    """Show the page at this address."""
    if address.startswith("/"):
        address = address[1:]
    if address.endswith("/"):
        address = address[:-1]

    try:
        page = Page.objects.get(address=address)
    except Page.DoesNotExist:
        return HttpResponseRedirect('/wiki/_edit/' + address)

    return render(request, "wiki/page.html", context=dict(page=page))

def edit(request, address):
    if address.startswith("/"):
        address = address[1:]
    if address.endswith("/"):
        address = address[:-1]

    try:
        page = Page.objects.get(address=address)
    except Page.DoesNotExist:
        page = None

    initial = {}
    if page:
        initial["title"] = page.title
        initial["content"] = page.content

    if request.method == 'POST':
        form = PageForm(request.POST, initial=initial)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            user = request.user
            user = user if user.is_authenticated() else None
            page = Page.objects.create_or_update_content(address, user, content)
            page.title = title
            page.save()
            return HttpResponseRedirect('/wiki/' + address)
    else:
        form = PageForm(initial=initial)

    return render(request, "wiki/edit.html", {'form': form, 'address': address, "page": page})
