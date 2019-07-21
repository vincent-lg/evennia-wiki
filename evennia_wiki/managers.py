"""Managers for the wiki app."""

from django.db.models import Manager, ObjectDoesNotExist

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

    def create_root_page_if_necessary(self):
        """
        Create the root page if it doesn't already exist.

        This is mostly used internally to make sure the root page always
        exists, or exists as soon as it's needed.

        """
        from evennia import AccountDB
        try:
            self.get(address="")
        except ObjectDoesNotExist:
            superuser = AccountDB.objects.get(id=1)
            root = self.create_content("", superuser, DEFAULT_ROOT_PAGE)
            root.title = "Welcome to your new evennia-wiki root page"
            root.save()

DEFAULT_ROOT_PAGE = """
**Welcome** to your new root page on [evennia-wiki](https://github.com/vincent-lg/evennia-wiki), a simple wiki to be integrated into [Evennia games](www.evennia.com).

What to do now?  You could start by editing this page to remove this default content.  You will need to log into an account with enough privileges (your superuser is a good choice).

- What syntax to use?  Check evennia-wiki's [syntax](https://vincent-lg.github.io/evennia-wiki/syntax.html).
- How to add new pages?  Check the evennia-wiki's [documentation on writing in the wiki](https://vincent-lg.github.io/evennia-wiki/page.html).
- How is this wiki structured?  Check out evennia-wiki's [structure](https://vincent-lg.github.io/evennia-wiki/structure.html).
- How to read and write wiki pages from my Evennia code?  Check out evennia-wiki's [simple API](https://vincent-lg.github.io/evennia-wiki/api.html).
- Have another question?  Check out evennia-wiki's [documentation](https://vincent-lg.github.io/evennia-wiki).

> If you would like to contribute to this project, either by just suggesting features or contribute to its source code, feel free to drop by [evennia-wiki's Github page](https://github.com/vincent-lg/evennia-wiki).

**Enjoy!**

""".strip()
