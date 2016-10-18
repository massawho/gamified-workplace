from django import forms
from django.forms import (
    models as django_models,
    fields as django_fields,
    widgets as django_widgets)
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import SetPasswordForm
from django.forms.models import BaseInlineFormSet
from extra_views.advanced import InlineFormSet
from apps.utils.forms import widgets
from .questionnaire.models import Questionnaire, QuestionnaireType
from .questionnaire.forms import QuestionnaireFormMixin
from django.utils.translation import ugettext_lazy as _
from .models import Employee, Badge, Team, TeamQuestionnaire


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.employee

User = get_user_model()

class UserQuestionnaireForm(QuestionnaireFormMixin, forms.ModelForm):

    targets = UserModelChoiceField(
        queryset=User.objects.filter(is_staff=False)
    )
    questionnaire_type = django_models.ModelChoiceField(
        queryset=QuestionnaireType.objects.all(),
        disabled=True
    )


class BadgeForm(forms.ModelForm):

    employee = django_models.ModelChoiceField(
        queryset=Employee.objects.filter(user__is_staff=False)
    )

    class Meta:
        model = Badge
        fields = ['employee', 'received_at']

class SatisfactionQuestionnaireForm(QuestionnaireFormMixin, forms.ModelForm):

    targets = UserModelChoiceField(
        queryset=User.objects.all().filter(is_staff=False),
        disabled=True
    )
    questionnaire_type = django_models.ModelChoiceField(
        queryset=QuestionnaireType.objects.all(),
        disabled=True
    )

    def __init__(self, current_user, *args, **kwargs):
        super(QuestionnaireFormMixin, self).__init__(*args, **kwargs)
        queryset = self.fields['targets'].queryset.filter(id=current_user.id)
        self.fields['targets'].queryset = queryset

class TaskQuestionnaireForm(UserQuestionnaireForm):

    description = django_fields.CharField(
        required=True,
        widget = django_widgets.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': _('Task name')
            }
        )
    )

class QuestionnaireForm(forms.ModelForm):
    description = django_fields.CharField(
        required=True,
        widget = django_widgets.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': _('Task name')
            }
        )
    )
    questionnaire_type = django_models.ModelChoiceField(
        queryset=QuestionnaireType.objects.all(),
        disabled=True
    )

    class Meta:
        model = Questionnaire
        fields = ['description', 'questionnaire_type']


class TeamQuestionnaireForm(forms.ModelForm):
    team = django_models.ModelChoiceField(
        queryset=Team.objects.filter(ended_at=None),
        required=True
    )

    def __init__(self, current_user, *args, **kwargs):
        super(TeamQuestionnaireForm, self).__init__(*args, **kwargs)
        queryset = self.fields['team'].queryset.exclude(members__id=current_user.id)
        self.fields['team'].queryset = queryset
        try:
            if kwargs['initial']['team']:
                self.fields['team'].disabled = True
        except KeyError:
            pass

    class Meta:
        model = TeamQuestionnaire
        fields = ['team']

class TeamQuestionnaireInline(InlineFormSet):
    model = TeamQuestionnaire
    form_class = TeamQuestionnaireForm
    extra = 1

    def get_formset_kwargs(self):
        kwargs = super(TeamQuestionnaireInline, self).get_formset_kwargs()
        kwargs['form_kwargs'] = {
            'empty_permitted': False,
            'current_user': self.request.user,
            'initial': {'team': self.kwargs['team_id']}
        }
        return kwargs


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

class UpdateLoginForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(UpdateLoginForm, self).__init__(instance=user.employee, *args, **kwargs)
        self.user = user
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name

    first_name = forms.CharField(
        label=_("First name"),
        required=True,
        label_suffix='',
        widget = django_widgets.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': _('First name')
            }
        ))
    avatar = forms.ImageField(
        label=_("Avatar"),
        label_suffix='',
        widget = django_widgets.FileInput(
            attrs = {
                'class': 'form-control'
            }
        ))
    last_name = forms.CharField(
        label=_("Last name"),
        required=True,
        label_suffix='',
        widget = django_widgets.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': _('First name')
            }
        ))
    nickname = forms.CharField(
        label=_("Nickname"),
        required=True,
        label_suffix='',
        widget = django_widgets.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': _('Nickname')
            }
        ))

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'nickname', 'avatar']

    def save(self, commit=True):
        user = self.user
        if commit:
            user.save()
        return user, super(UpdateLoginForm, self).save(commit)

class FirstLoginForm(UpdateLoginForm):

    def __init__(self, *args, **kwargs):
        self._meta.fields.append('username')
        super(FirstLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = self.user.username

    username = forms.CharField(
        label=_("User"),
        required=True,
        label_suffix='',
        widget = django_widgets.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': _('User')
            }
        ))

    date_of_birth = forms.DateField(
        label=_("Date of birth"),
        required=True,
        label_suffix='',
        widget = django_widgets.DateInput(
            attrs = {
                'class': 'form-control',
                'placeholder': _('Date of birth'),
                'data-mask': '99/99/9999'
            }
        ))
    new_password1 = forms.CharField(
        label=_("New password"),
        required=True,
        label_suffix='',
        widget = django_widgets.PasswordInput(
            attrs = {
                'class': 'form-control',
                'placeholder': _('Password')
            }
        ))
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        required=True,
        label_suffix='',
        widget = django_widgets.PasswordInput(
            attrs = {
                'class': 'form-control',
                'placeholder': _('Password confirmation')
            }
        ))

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    _("The two password fields didn't match."),
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.instance)
        return password2

    def save(self, commit=True):
        user, employee = super(FirstLoginForm, self).save(False)
        password = self.cleaned_data["new_password1"]
        user.set_password(password)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.username = self.cleaned_data["username"]
        employee.first_login = False
        if commit:
            user.save()
            employee.save()
        return user, employee
