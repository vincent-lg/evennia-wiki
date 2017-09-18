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

    if not page.access(request.user, "read"):
        return render(request, "wiki/cant_read.html")

    return render(request, "wiki/page.html", context=dict(page=page))

def edit(request, address):
    if address.startswith("/"):
        address = address[1:]
    if address.endswith("/"):
        address = address[:-1]

    # We try to find the parent.  Creating a page without parent isn't possible.
    parent = None
    if "/" in address:
        parent = address.rsplit("/", 1)[0]
        try:
            parent = Page.objects.get(address=parent)
        except Page.DoesNotExist:
            parent = None

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
            new_page = Page.objects.create_or_update_content(address, user, content)
            new_page.title = title
            if parent and not page:
                new_page.can_write = parent.can_write
                new_page.can_read = parent.can_read
            print "update", new_page
            if new_page.access(user, "write"):
                print "saving"
                new_page.save()
            return HttpResponseRedirect('/wiki/' + address)
    elif parent and not parent.access(request.user, "write"):
        return HttpResponseRedirect('/wiki/' + address)
    elif page and not page.access(request.user, "read"):
        return HttpResponseRedirect('/wiki/' + address)
    else:
        form = PageForm(initial=initial)

    return render(request, "wiki/edit.html", {'form': form, 'address': address, "page": page, "parent": parent})
