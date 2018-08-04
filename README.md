# evennia-wiki

A simple wiki for `Evennia`, simple to install within an [Evennia](www.evennia.com) game.

## Installation

For the time being, you should install from source.  Assuming you are in
this directory (where the `README.md` file is):

    python setup.py install

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

