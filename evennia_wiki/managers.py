"""Managers for the wiki app."""

from django.db.models import Manager

class PageManager(Manager):

    """Custom manager for the Page model.

    This manager allows to:
        - Create both pages and revisions.
        - Update a page by adding a new revision.
        - Update or create a page with some content.

    """

    def create_content(self, address, owner, content):
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
        page.check_address()
        revision = page.revision_set.create(page=page, content=content, owner=owner)
        page.update_html(content)
        return page

    def update_content(self, address, owner, content):
        """
        Update the content of an existing article.

        Args:
            address (str): the address of an existing page.
            owner (User): the owner of the revision.
            content (str): the content of the revision to be created.

        """
        page = self.get(address=address)
        page.check_address()
        revision = page.revision_set.create(page=page, content=content, owner=owner)
        page.update_html(content)
        return page

    def create_or_update_content(self, address, owner, content,
            force_update=True):
        """
        Create or update a page with content.

        Args:
            address (str): the address of a page (existing or not).
            owner (User): the owner of the revision.
            content (str): the content of the revision to be created.
            force_update (bool, optional): force updating the article
                    even if the content is not different.

        Note:
            The `force_update` argument, if set to `False`, will not
            update the page if the content isn't different from the
            one specified in argument.  This avoids creating a lot
            of revisions whether no change has taken place.

        """
        try:
            page = self.get(address=address)
        except self.model.DoesNotExist:
            return self.create_content(address, owner, content)
        else:
            # The page exist
            if force_update or page.content != content:
                page = self.update_content(address, owner, content)

            return page
