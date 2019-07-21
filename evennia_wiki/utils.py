"""Utility functions to control the wiki's content from your Evennia game."""

from evennia_wiki.models import Page

def get_content(address):
    """
    Get an existing wiki page, return it or None if the page doesn't exist.

    Args:
        address (str): the page's absolute address.

    Returns:
        page (Page): the page at this address if found or None.

    """
    if address.startswith("/"):
        address = address[1:]

    try:
        page = Page.objects.get(address=address)
    except Page.DoesNotExist:
        page = None

    return page

def create_content(address, owner, content):
    """
    Create a new page with some content.

    Args:
        address (str): the new page's absolute address.
        owner (Account): the owner of the page to be created.
        content (str): the Markdown content of the first revision.

    Returns:
        page (Page): the newly-created page.

    """
    if address.startswith("/"):
        address = address[1:]

    return Page.objects.create_content(address, owner, content)

def update_content(address, owner, content):
    """
    Update an existing page's content (write a new revision).

    Args:
        address (str): the existing page's absolute address.
        owner (Account): the owner of the revision to add.
        content (str): the Markdown content of the new revision.

    Returns:
        page (Page): the updated page.

    """
    if address.startswith("/"):
        address = address[1:]

    return Page.objects.update_content(address, owner, content)

def create_or_update_content(address, owner, content, force_update=True):
    """
    Create a new page if it doesn't exist, or update an existing content.

    Args:
        address (str): the new or existing page's absolute address.
        owner (Account): the owner of the revision to add.
        content (str): the Markdown content of the new revision.
        force_update (bool, optional): if True, create a new revision even
                if the old's revision had the exact same content.

    Returns:
        page (Page): the created or updated page.

    """
    if address.startswith("/"):
        address = address[1:]

    return Page.objects.create_or_update_content(address, owner, content, force_update)
