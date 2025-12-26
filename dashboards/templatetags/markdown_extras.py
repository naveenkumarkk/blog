from django import template
import markdown

register = template.Library()
@register.filter
def render_markdown(text):
    return markdown.markdown(
        text or "",
        extensions=["fenced_code", "codehilite", "tables", "nl2br", "sane_lists"]
    )

@register.filter
def shout(value):
    return value.upper()