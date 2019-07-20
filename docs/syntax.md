# evennia-wiki syntax

evennia-wiki uses the [Markdown](https://en.wikipedia.org/wiki/Markdown) language to write pages.  You'll find a useful [Markdown cheatsheet here](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet).

The simple Markdown syntax is used by evennia-wiki with some additions that are listed on this page.

## Wiki links

It is possible to link to wiki pages from other wiki pages.  Two usages are possible, both using the Markdown link syntax:

- Relative: most of the time, you will specify the relative page address leading to its content.  For instance, if you edit `/rule` and have a `/rule/1` page (which is a child page of `/rule`), you could add a link to the first rule like this: `[rule 1](1)` .  Here, you specify only the relative path leading to the page from the page address on which the link is present.
- Absolute: it is also possible to link to a page, specifying the absolute page address leading to it.  From anywhere on the wiki, to add a page to the same `/rule/1` page, you could write something like: `[rule 1](/rule/1)` .  This second syntax, although longer, has the advantage that the page on which you actually stand has no importance, the link will be valid no matter what.  Since evennia-wiki enforces its hierarchy and makes it more difficult to move pages around, this advantage is not as important.

## Tables

evennia-wiki supports the Markdown extended syntax for tables:

```
| Column 1 | Column 2 | Column 3 |
| -------- | -------- | -------- |
| value 1  | value 2  | value 3  |
| value 4  | value 5  | value 6  |
```

You can also use the syntax to align table columns to the right or the center.

## Table of contents

You can include a table of content.  On a paragraph of its own, include the following:

    [TOC]

Then the evennia-wiki will build a list of headings in your page and create anchor links to them.

