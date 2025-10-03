from django import template
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify

register = template.Library()


@register.filter
def markdownx(content):  # pragma: no cover
    """
    Convert Markdown content to HTML using MarkdownX's markdownify function.
    """
    if content:
        return mark_safe(markdownify(content))
    return ""
