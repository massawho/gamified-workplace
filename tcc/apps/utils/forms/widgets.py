from django.forms import widgets
from django.forms.utils import flatatt
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.html import format_html


class SlideiOSWidget(widgets.TextInput):

    def __init__(self, max=100, attrs=None):
        extra_attrs = {
            'data-slide-ios': True,
            'data-slider-max': max
        }

        if attrs:
            attrs.update(extra_attrs)
        else:
            attrs = extra_attrs
        super(SlideiOSWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if value is None or value is '':
            value = '0'
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        final_attrs['data-slider-value'] = value
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self.format_value(value))
        return format_html('<input{} />', flatatt(final_attrs))
