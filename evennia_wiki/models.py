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


class Revision(models.Model):

    """A wiki revision, with an author and text."""

    page = models.ForeignKey(Page, null=True, blank=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(AccountDB, null=True, blank=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField("created on", auto_now=True, auto_now_add=True)
    content = models.TextField()
