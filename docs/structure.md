# evennia-wiki structure

evennia-wiki is based around a simple page structure.  Each page (wiki article) is set in a specific place and can have a parent and child pages.

## Parent page

A page always has a parent page, except for the root page.  The root page's address (its location) is `/`, meaning it's at the top of the hierarchy.

A child page of the root page may have an address of `/rule` for instance.  This page `/rule` has for parent page the root page (`/`).

If you create a child page of this `/root` page, of address `1` for instance, this page will have for full address `/rule/1` and for parent page `/rule`.

This simple hierarchy of parent page is easy to understand and connect to most wiki architectures.  The points to remember here are:

- Each page has an address.  This address is not the page title.  When creating a page, you'll be asked for the page sub-address (that is, the part after the parent address and a slash).  See [page creation](page.md#create-a-page] for more details.
- Each page always has a parent, except for the root page.  The root page's address is `/` and it's at the top of the hierarchy.

## Child pages

Similarly, a page can have child pages.  The `/rule` page could have for child pages `/rule/1` and `/rule/2`.  The root page itself will have for child page (in this example) only `/rule`.

You can create new child pages on any wiki page.  To do so, click on the "child pages" sub-menu.  In the address, enter the sub-address of the future page.  For instance, if you're on `/rule` and want to add `/rule/1`, just type `1` in this field.  Click on create.

A page can have zero, one or several child pages.
