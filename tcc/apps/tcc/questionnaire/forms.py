from django import forms
from django.forms import models
from extra_views.advanced import InlineFormSet
from .models import Answer, EngagementMetric, Questionnaire, QuestionnaireType
from apps.utils.forms import widgets


class AnswerForm(forms.ModelForm):
    engagement_metric = models.ModelChoiceField(
        queryset=EngagementMetric.objects.all(),
        disabled=True
    )
    class Meta:
        model = Answer
        fields = ['value', 'engagement_metric']
        widgets = {
            'value': widgets.SlideiOSWidget(max=10)
        }

class AnswersInline(InlineFormSet):
    model = Answer
    form_class = AnswerForm

class QuestionnaireFormMixin(object):
    questionnaire_type = models.ModelChoiceField(
        queryset=QuestionnaireType.objects.all(),
        disabled=True
    )
    class Meta:
        model = Questionnaire
        fields = ['targets', 'description', 'questionnaire_type']

    def _save_m2m(self):
        self.cleaned_data['targets'] = [self.cleaned_data['targets']]
        super(QuestionnaireFormMixin, self)._save_m2m()

    def __init__(self, current_user, *args, **kwargs):
        super(QuestionnaireFormMixin, self).__init__(*args, **kwargs)
        queryset = self.fields['targets'].queryset.exclude(id=current_user.id)
        self.fields['targets'].queryset = queryset
        try:
            if kwargs['initial']['targets']:
                self.fields['targets'].disabled = True
        except KeyError:
            pass
