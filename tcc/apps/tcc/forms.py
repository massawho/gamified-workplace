from django.forms.models import BaseInlineFormSet


class EmployeeFormSet(BaseInlineFormSet):
    """
    Generates an inline formset that is required
    """

    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        form = super(EmployeeFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form


class EngagementMetricConfigFormSet(BaseInlineFormSet):
    """
    Generates an inline formset that is required
    """

    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        form = super(EngagementMetricConfigFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form
