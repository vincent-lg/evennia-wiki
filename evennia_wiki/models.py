# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from evennia.accounts.models import AccountDB
from markdown import Markdown

from managers import PageManager

# Constants
MARKDOWN = Markdown()

class Page(models.Model):

    """A wiki page, with a history of revisions."""

    address = models.CharField(max_length=200)
    title = models.CharField(max_length=200, default="")
    created_on = models.DateTimeField("created on", auto_now_add=True)
    objects = PageManager()
    author = models.ForeignKey(AccountDB, null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def last_revision(self):
        """Return the last revision, if any, or None."""
        return self.revision_set.order_by("created_on").last()

    @property
    def content(self):
        """Return the text content of the last revision.

        Note:
            This returns the text content (unprocessed-markdown str)
            of the last revision, or an empty string.

        """
        last = self.last_revision
        if last:
            return last.content
        else:
            return ""

    @property
    def html(self):
        """Return the HTML str of the last revision."""
        MARKDOWN.reset()
        return MARKDOWN.convert(self.content)

    @property
    def parent_address(self):
        """Return the direct parent address deduced from the current address.

        If the address is "a/b/c", the parent's address will be "a/b".
        A page with an address like "a" will have the root (empty
        string) as a parent address.  The root itself will have no
        parent (None).

        """
        address = self.address
        if address.startswith("/"):
            address = address[1:]
        if address.endswith("/"):
            address = address[:-1]

        if "/" in address:
            # Return everything before the last / sign
            return address.rsplit("/", 1)[0]
        elif address:
            return ""
        else:
            return None

    @property
    def parent(self):
        """Return the parent page or None."""
        address = self.parent_address
        try:
            parent = Page.objects.get(address=address)
        except Page.DoesNotExist:
            parent = None

        return parent

    @property
    def parent_addresses(self):
        """Return the succession of parent addresses.

        Return a list of str (each element of the list being a piece
        of URI split by the / sign).  This list can be empty or
        contain only an empty string.  If the list is not empty, the
        first element is always the root class (an empty string).

        """
        address = self.address
        if not address.startswith("/"):
            address = "/" + address
        if address.endswith("/"):
            address = address[:-1]

        if address:
            return address.split("/")[:-1]

        return []

    @property
    def parents(self):
        """Return all the parent pages, ordered by hierarchy.

        If this is not the root page (with an empty address), then
        the first list element will be the root.  Next will be all
        pages in the hierarchy of this page.  For instance, if the
        address of this page is: "story/fairy/001", then the list will
        be: `[<RootPage>, <Page story>, <Page fairy>]`.

        """
        addresses = self.parent_addresses
        q = models.Q()
        for address in addresses:
            q |= models.Q(address=address)

        if addresses:
            pages = Page.objects.filter(q)

            # Order the pages in a hierarchy
            pages = sorted(list(pages), key=lambda page: addresses.index(page.address))
        else:
            pages = []

        return pages

    def __str__(self):
        address = self.address
        if address:
            return self.address
        else:
            return "/"


class Revision(models.Model):

    """A wiki revision, with an author and text."""

    page = models.ForeignKey(Page, null=True, blank=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(AccountDB, null=True, blank=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField("created on", auto_now_add=True)
    content = models.TextField()
