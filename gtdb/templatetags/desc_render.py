from django import template
from django.template.defaultfilters import stringfilter
from pybb.defaults import urlize, smile_it, render_bbcode
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
@stringfilter
def render(value):
    return mark_safe(urlize(smile_it(render_bbcode(value, exclude_tags=['size', 'center']))))
