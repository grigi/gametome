from django import template
from django.template.defaultfilters import stringfilter
from pybb.defaults import urlize, render_bbcode, PYBB_SMILES_PREFIX
from django.utils.safestring import mark_safe
from django.conf import settings
import re
from markdown import Markdown

ALL_SMILES = getattr(settings, 'ALL_SMILES', {})

register = template.Library()

def smile_it(str):
    s = str
    for smile, url in ALL_SMILES.items():
        s = s.replace(' %s' % smile, ' <img src="%s%s%s" alt="smile" />' % (settings.STATIC_URL, PYBB_SMILES_PREFIX, url))
        s = s.replace('%s ' % smile, '<img src="%s%s%s" alt="smile" /> ' % (settings.STATIC_URL, PYBB_SMILES_PREFIX, url))
    return s

@register.filter
@stringfilter
def render(value):
    #return mark_safe(urlize(smile_it(render_bbcode(value, exclude_tags=['size', 'center']))))
    return mark_safe(urlize(smile_it(Markdown(safe_mode='escape').convert(value))))
