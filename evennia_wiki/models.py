# -*- coding: utf-8 -*-

from datetime import datetime
import re

from django.db import models
from django.conf import settings
from django.utils.timezone import now
from evennia.accounts.models import AccountDB
from evennia.utils.utils import time_format
from evennia_wiki.markdown_engine import ENGINE
from evennia_wiki.managers import PageManager

## Constants
_PERMISSION_HIERARCHY = ["anonymous"] + [pe.lower() for pe in settings.PERMISSION_HIERARCHY]
RE_PATH = re.compile(r"^[A-Za-z0-9_/-]*$")

class Page(models.Model):

    """A wiki page, with a history of revisions."""

    objects = PageManager()
    address = models.CharField(max_length=2000, db_index=True, unique=True)
    title = models.CharField(max_length=200, default="")
    created_on = models.DateTimeField("created on", auto_now_add=True)
    author = models.ForeignKey(AccountDB, null=True, blank=True, on_delete=models.SET_NULL)
    html = models.TextField(default="")
    can_write = models.CharField(max_length=50, default="Developer")
    can_read = models.CharField(max_length=50, default="Developer")

    @property
    def last_revision(self):
        """Return the last revision, if any, or None."""
        return self.revision_set.order_by("created_on").last()

    @property
    def last_modified_ago(self):
        """Return the X {unit}{s} ago."""
        revision = self.last_revision
        if revision:
            seconds = (now() - revision.created_on).total_seconds()
            ago = time_format(seconds, 4)
            return "{} ago".format(ago)

        return "never"

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

    @property
    def children(self):
        """Return the direct children of  this page."""
        address = self.address
        if address:
            address += "/"

        # Escape the address for re matching
        addres = re.escape(address)
        regex = "^" + address + "[^/]+$"
        children = Page.objects.filter(address__regex=regex).order_by("address")
        return list(children)

    @property
    def part_address(self):
        """Return the last part of the address after the last /."""
        address = self.address
        if address.startswith("/"):
            address = address[1:]
        if address.endswith("/"):
            address = address[:-1]

        if not address:
            return "root"
        elif "/" in address:
            return address.rsplit("/", 1)[1]
        else:
            return address

    def __str__(self):
        address = self.address
        if address:
            return self.address
        else:
            return "/"

    def check_address(self):
        """Check that the current address is compliant."""
        if RE_PATH.search(self.address) is None:
            raise ValueError("{} isn't an acceptable path".format(repr(self.address)))

    def update_html(self, plain_text):
        """Update the HTML field with the plain text markdown."""
        ENGINE.reset()
        self.html = ENGINE.convert(self.content)

    def access(self, user, can="read"):
        """Return True if the user can access the page.

        Args:
            user (AccountDB): the user accessing the page.
            can (str): what to access (can be  read" or "write").

        Returns:
            access (bool): can the user access this page to read or write?

        """
        if can == "read":
            permission = self.can_read
        elif can == "write":
            permission = self.can_write
        else:
            raise ValueError("Invalid access: {}".format(can))

        # However, the settings for `WIKI_ALLOW_*` takes precedence
        permission = getattr(settings, f"WIKI_CAN_{can.upper()}", permission)
        permission = permission.lower()
        if user is None or not user.is_authenticated:
            perms_object = ["anonymous"]
        else:
            perms_object = user.permissions.all()

        if permission in perms_object:
            # simplest case - we have direct match
            return True

        if permission in _PERMISSION_HIERARCHY:
            # check if we have a higher hierarchy position
            hpos_target = _PERMISSION_HIERARCHY.index(permission)
            return any(1 for hpos, hperm in enumerate(_PERMISSION_HIERARCHY)
                       if hperm in perms_object and hpos_target < hpos)

        return False



class Revision(models.Model):

    """A wiki revision, with an author and text."""

    page = models.ForeignKey(Page, null=True, blank=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(AccountDB, null=True, blank=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField("created on", auto_now_add=True)
    content = models.TextField()
