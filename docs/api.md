# evennia-wiki API

evennia-wiki offers easy-to-use entry points into the wiki, so you can access and modify wiki pages very simply from your code.

## Retrieving a page object

`evennia_wiki.utils.get_content(address)`: get the page at the specific address.  No permission control is done (it is assumed you have all privileges).

```python
from evennia_wiki.utils import get_content

root = get_content("/") # get the root page or None
rule = get_content("/rule") # Get the /rule page or None

if rule:
    title = rule.title
    address = rule.address
    datetime = rule.created_on
    author = rule.author
    # do not modify these fields manually
    markdown = rule.content # last markdown content of the page
    html = rule.html # last HTML content of this page
```

The `content` and `html` attributes are automatic caches of the last revision's Markdown and HTML content.  Updating them manually is not advisable, rather, use the `update_content` or `create_or_update_content` utilities.

## Updating content

Three utility functions are provided to create pages or update contents.  The first one is probably the one you want to use as it's more generic:

- `evennia_wiki.utils.create_or_update_content(address, owner, content, force_update=True)`: create a page or update its content if it exists.  A new revision will be created, with the owner of this revision being the owner specified in this utility function.  `content` is the markdown content to be placed in the page.  The `force_update` flag, if set to `True`, will create a revision even if the page currently has the same content.  Usually, you will want to set this flag to `False` as there's no need to create a new revision if the content hasn't changed.
- `evennia_wiki.utils.create_content(address, owner, content)`: create a new page with an unused address.  The owner is the account that will own the page (be its author) and owner of the first revision.  The `content` is the Makdown content that will be used.
- `evennia_wiki.utils.update_content(address, owner, content)`: almost identical to `create_content`, except the page has to exist.  The `owner` will be the owner of the future revision.

Here's a very basic usage example:

```python
from evennia import AccountDB
from evennia_wiki.utils import create_or_update_content

superuser = AccountDB.objects.get(id=1) # superuser always has ID 1
text = """
Welcome to my **game**.

It's really great!

- Check it out using the webclient.
- Built with [Evennia](www.evennia.com).

"""

page = create_or_update_content("/", superuser, text, force_update=False)
page.title = "The root page"
page.save()
```

