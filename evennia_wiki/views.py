# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render

from evennia_wiki.forms import PageForm
from evennia_wiki.models import Page

def view(request, address=""):
    """Show the page at this address, handling permission.

    If the page doesn't exist, create it if allowed:
        The superuser can do everything.
        The user can edit the parent.
    If the page exists, display it if allowed:
        The superuser can do everything.
        The user can read the page.

    """
    user = request.user if request.user.is_authenticated else None
    if address.startswith("/"):
        address = address[1:]
    if address.endswith("/"):
        address = address[:-1]

    # we try to find the parent. This information is used to see if the user can create the page.
    parent = None
    if "/" in address:
        parent = address.rsplit("/", 1)[0]
    else:
        parent = ""

    Page.objects.create_root_page_if_necessary()
    try:
        parent = Page.objects.get(address=parent)
    except Page.DoesNotExist:
        parent = None

    # try to get the page itself
    try:
        page = Page.objects.get(address=address)
    except Page.DoesNotExist:
        if user and user.is_superuser:
            return HttpResponseRedirect('/wiki/_edit/' + address)
        elif parent and parent.access(user, "write"):
            return HttpResponseRedirect('/wiki/_edit/' + address)

        return render(request, "wiki/cant_read.html")

    if not page.access(request.user, "read"):
        return render(request, "wiki/cant_read.html")

    context = {
            "page": page,
            "can_read": page.access(user, "read"),
            "can_write": page.access(user, "write"),
    }

    return render(request, "wiki/page.html", context=context)

def edit(request, address):
    """Try to edit the given page, handling permissions.

    If the page doesn't exist, create it if allowed:
        The superuser can do everything.
        The user can edit the parent.
    If the page exists, update it if allowed:
        The superuser can do everything.
        The user can edit the page.

    """
    if address.startswith("/"):
        address = address[1:]
    if address.endswith("/"):
        address = address[:-1]

    # we try to find the parent.  Creating a page without parent isn't possible.
    parent = None
    if "/" in address:
        parent = address.rsplit("/", 1)[0]
    else:
        parent = ""

    try:
        parent = Page.objects.get(address=parent)
    except Page.DoesNotExist:
        parent = None

    # try to get the page itself, which might exist
    try:
        page = Page.objects.get(address=address)
    except Page.DoesNotExist:
        page = None

    initial = {}
    if page:
        initial["title"] = page.title
        initial["content"] = page.content

    if request.method == 'POST':
        # the form has been sent, use the different access rights
        form = PageForm(request.POST, initial=initial)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            user = request.user
            user = user if user.is_authenticated else None
            can = False
            if user and user.is_superuser:
                # the superuser can do it all
                can = True
            elif parent and page is None and parent.access(user, "write"):
                # the page doesn't exist, but the parent does, and the user can edit it
                can = True
            elif page and page.access(user, "write"):
                # the page already exist and the user can edit it
                can = True

            if can:
                new_page = Page.objects.create_or_update_content(address, user, content)
                new_page.title = title
                if parent is not None and page is None:
                    new_page.can_write = parent.can_write
                    new_page.can_read = parent.can_read
                new_page.save()

            return HttpResponseRedirect('/wiki/' + address)
    else:
        form = PageForm(initial=initial)

    return render(request, "wiki/edit.html", {'form': form, 'address': address, "page": page, "parent": parent})
