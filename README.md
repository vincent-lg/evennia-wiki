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
    url(r'^wiki/', include('evennia_wiki.urls',
            namespace='wiki', app_name='wiki')),
]
```

Don’t forget to run `evennia migrate` after that.

## Usage

You can now run your game:

    evennia start

Go to your website: http://localhost:4001/wiki/ .
