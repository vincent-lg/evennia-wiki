"""Class containing the generic markdown engine used by evenniq_wiki."""

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


ENGINE = MarkdownEngine()
