# evennia-wiki installation

Using the evennia-wiki is easy once an [Evennia](www.evennia.com) game has been configured.  To enter the following commands, activate your virtual environment (the one you created for your [Evennia game](www.evennia.com).

## Installing from Pypi

evennia-wiki is hosted on [Pypi](https://pypi.org/project/evennia-wiki/).  You can easily install it with pip:

    pip install evennia-wiki

## Initial setup

### Setting file

Open your setting file, `server/conf/settings.py`.  That's your public settings which will by read by anyone if your code is pushed to a public repository.  You probably don't mind, since the following settings are not sensitive.

Before importing the `secret_sdettings.py` file, add a section (it might be just below your `SERVERNAME = ...` directive:

```python
INSTALLED_APPS += (
        "evennia_wiki",
)
```

In other words, you just need to add `"evennia_wiki"` to your installed apps, since the Evennia wiki has its own models which will need migration.

### URLs

Then open your default URLs in `web/urls.py`.  In the `custom_patterns` list, add a new entry to point to the wiki app.  The list should look something like this:

```python
custom_patterns = [
    # url(r'/desired/url/', view, name='example'),
    url(r'^wiki/', include('evennia_wiki.urls')),
]
```

This will add the `/wiki/` URL (and sub-pages) to your game website.

### Migrations

Then run the migrations.  evennia-wiki adds its own models and Evennia needs to know about them:

    python manage.py migrate

### Test your new wiki

Start your Evennia game.  Connect to http://localhost:4001/wiki/ as a superuser.  You'll be prompted to edit the root page.  This is a wiki page that's required by the wiki, sort of your parent of all other pages.

## Where to now?

- [Understanding evennia-wiki's structure](structure.md).
- [Creating content in the wiki](page.md).
- [What syntax to use to write in the wiki?](syntax.m).
- [Setting permissions on evennia-wiki](permissions.md).
- [Changing default templates of wiki pages](template.md).

