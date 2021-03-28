from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.filter(name='markdown_to_text')
def markdown_to_text_format(text):
    return mark_safe(text)
