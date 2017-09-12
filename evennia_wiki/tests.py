# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from evennia_wiki.models import Page, Revision

class TestPages(TestCase):

    def test_hierarchy(self):
        """Test the hierarchy of wiki pages."""
        root = Page.objects.create(address="")
        music = Page.objects.create(address="music")
        jazz = Page.objects.create(address="music/jazz")
        folk = Page.objects.create(address="music/folk")

        # TEst the single parent of each page
        self.assertEqual(music.parent, root)
        self.assertEqual(jazz.parent, music)
        self.assertEqual(folk.parent, music)

        # Test multiple parents
        self.assertEqual(music.parents, [root])
        self.assertEqual(jazz.parents, [root, music])
        self.assertEqual(folk.parents, [root, music])

    def test_content(self):
        """Test to add/edit content quickly."""
        root = Page.objects.create_content("", None, "This is the root page.")
        self.assertEqual(root.content, "This is the root page.")

        # Try to update the content of this page
        Page.objects.update_content("", None, "Something else.")
        self.assertEqual(root.content, "Something else.")

        # Try creating or updating regardless
        page = Page.objects.create_or_update_content("page", None,
                "This is a page.")
        self.assertEqual(page.content, "This is a page.")
        page = Page.objects.create_or_update_content("page", None,
                "This is another content.")
        self.assertEqual(page.content, "This is another content.")
