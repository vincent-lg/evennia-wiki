"""Managers for the wiki app."""

from django.db.models import Manager

class PageManager(Manager):

    """Custom manager for the Page model.

    This manager allows to:
        - Create both pages and revisions.
        - Update a page by adding a new revision.
        - Update or create a page with some content.

    """

    def create_with_content(self, address, owner, content):
        """Create a wiki page with content.

        Args:
            address (str): the address of the new page.
            owner (User): the owner of the revision.
            content (str): the content of the revision to be created.

        Note:
            The owner of the revision to be created will also be the
            author of this article.

        """
        page = self.create(address=address, author=owner)
        page.save()
        revision = page.revision_set.create(page=page, content=content, owner=owner)
        return page
