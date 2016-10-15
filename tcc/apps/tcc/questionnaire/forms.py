from django import forms
from django.forms import models
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


class QuestionnaireForm(object):
    questionnaire_type = models.ModelChoiceField(
        queryset=QuestionnaireType.objects.all(),
        disabled=True
    )
    class Meta:
        model = Questionnaire
        fields = ['targets', 'description', 'questionnaire_type']

    def _save_m2m(self):
        self.cleaned_data['targets'] = [self.cleaned_data['targets']]
        super(QuestionnaireForm, self)._save_m2m()

    def __init__(self, current_user, *args, **kwargs):
        super(QuestionnaireForm, self).__init__(*args, **kwargs)
        queryset = self.fields['targets'].queryset.exclude(id=current_user.id)
        self.fields['targets'].queryset = queryset
