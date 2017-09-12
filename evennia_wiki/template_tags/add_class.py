from django import template

register = template.Library()


@register.filter(name='addclass')
def addclass(value, arg):
    """Add a class to a widget."""
    return value.as_widget(attrs={'class': arg})
