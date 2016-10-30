from django.template import Library
from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
import re


register = Library()

@register.filter
def rank_class(value):
    if value == 1:
        return 'bronze'
    elif value == 2:
        return 'silver'
    elif value == 3:
        return 'gold'
    else:
        return 'blue'

@register.filter
def get_answer_value_field(form, position):
    return form["answer_value_%d" % position]

@register.filter
def is_missing_questionnaire(team, user):
    return team.missing_questionnaire(user.employee)

@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname) + '$'
    except NoReverseMatch:
        pattern = '^' + pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'nav-active active'
    return ''
