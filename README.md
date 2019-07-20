# evennia-wiki

A simple wiki for `Evennia`, simple to install within an [Evennia](www.evennia.com) game.

## Installation

You have to install Evennia beforehand.  Once done, to add the Wiki, install from pypi:

    pip install evennia_wiki

Then, in your Evennia folder, edit `server/conf/settings.py` to add
the installed app:

```python
INSTALLED_APPS += (
        # ...
        "evennia_wiki",
)
```

Finally, in `web/urls.py`, you should add the custom URL:

```python
custom_patterns = [
    # ...
    url(r'^wiki/', include('evennia_wiki.urls', namespace='wiki')),
]
```

Don’t forget to run `evennia migrate` after that.

## Usage

You can now run your game:

    evennia start

Go to your website: http://localhost:4001/wiki/ .

## Settings

By default, the wiki is off-limit to players.  Only authenticated builders have access to it, to write it and read it.  You can change these defaults.

The current possibility is to change this default for every page.  It is not possible to do it for a specific page.  Go to your `settings.lpy` file and change one of these settings:

- `WIKI_CAN_READ`: who can read the wiki? Set to `"builder"` by default. Change it to `"anonymous"` to allow anonymous visitors to read your wiki (but not edit it).
- `WIKI_CAN_WRITE`: who can write your wiki?  Set to `"builder"` by default.  For the time being, anonymous users cannot edit a wiki page, so you need to set it to a group of authenticated users (like `"builder"`  or `"admin"`).

