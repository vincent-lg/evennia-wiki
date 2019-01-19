"""Class containing the generic markdown engine used by evenniq_wiki."""

from bs4 import BeautifulSoup
from markdown import Markdown

class MarkdownEngine(Markdown):

    """A special markdown engine for the evennia_wiki.

    This pre-loads some common extensions and allows some inner processing.

    """

    def __init__(self):
        super(MarkdownEngine, self).__init__(extensions=[
                'markdown.extensions.fenced_code',
                'markdown.extensions.footnotes',
                'markdown.extensions.tables',
                'markdown.extensions.toc',
        ])

    def convert(self, text):
        """Convert the text to HTML, changing some classes.

        1. Table elements will have classes table table-responsive table-striped
        2. Table headers will have the class thead-inverse
        3. Links elements will be re-mapped if absolute (beginning by /)

        """
        html = super(MarkdownEngine, self).convert(text)
        soup = BeautifulSoup(html, 'html.parser')

        # Add classes to tables
        for tag in soup.find_all("table"):
            tag["class"] = "table table-responsive table-striped"

        # Add classes to table headers
        for tag in soup.find_all("thead"):
            tag["class"] = "thead-inverse"

        # Change link location of pointing to /* . We assume an absolute
        # URL (/) means a wiki page.
        for tag in soup.find_all("a"):
            href = tag.get("href")
            if href and href.startswith("/"):
                tag["href"] = "/wiki" + href

        return str(soup)

ENGINE = MarkdownEngine()
