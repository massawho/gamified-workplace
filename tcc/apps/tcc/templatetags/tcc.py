from django.template import Library

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
