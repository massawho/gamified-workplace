from django.urls import reverse
from django.contrib import messages
from django.db import models
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from .models import (Product, Employee, Purchase, Team, Goal, TeamQuestionnaireControl,
    MANAGER_COLLABORATOR, COLLABORATOR_SATISFACTION, TASK_FEEDBACK)
from django.views.generic import DetailView
from extra_views import FormSetView
from rules.contrib.views import PermissionRequiredMixin
from .questionnaire.forms import AnswersInline
from .questionnaire.models import EngagementMetric, Answer, Questionnaire, update_score
from .questionnaire.signals import update_score as update_score_signal
from .questionnaire.views import GenericQuestionnaireView
from .forms import (UserQuestionnaireForm, SatisfactionQuestionnaireForm, FirstLoginForm,
        TeamQuestionnaireForm, TeamQuestionnaireInline, QuestionnaireForm, UpdateLoginForm,
        TaskQuestionnaireForm, PeerToPeerQuestionnaireForm)
from .signals import update_money


@login_required
def dashboard(request):
    if not request.user.is_staff:
        goals = Goal.objects.all()
        badges = request.user.employee.badge_set.all()
        featured_products = Product.objects.filter(is_active=True, is_featured=True)
        user_teams = request.user.employee.team_set.active()
        inventory = request.user.employee.get_inventory()
        engagement_metrics = Answer.objects \
            .values('engagement_metric', 'engagement_metric__name', 'engagement_metric__description',
                'engagement_metric__engagementmetricconfig__icon_class' ) \
            .filter(questionnaire__targets__id=request.user.pk,
                engagement_metric__engagementmetricconfig__is_staff=False) \
            .annotate(value=models.Avg('value'))

        return render(request, 'tcc/views/dashboard/user_dashboard.html', {
            'profile': request.user.employee,
            'featured_products': featured_products,
            'inventory': inventory,
            'user_teams': user_teams,
            'goals': goals,
            'badges': badges,
            'skill_list': engagement_metrics
        })
    else:
        employees = Employee.objects.filter(user__is_staff=False)

        teams = Team.objects.filter(ended_at=None)

        return render(request, 'tcc/views/dashboard/manager_dashboard.html', {
            'employees': sorted(employees, key=lambda employee: employee.points, reverse=True),
            'teams': teams,
        })


@login_required
@user_passes_test(lambda u: u.is_staff)
def profile(request, pk):
    employee = get_object_or_404(Employee, pk=pk, user__is_staff=False)

    user_teams = employee.team_set.active()
    inventory = employee.get_inventory()

    goals = Goal.objects.all()
    badges = employee.badge_set.all()

    engagement_metrics = Answer.objects \
            .values('engagement_metric', 'engagement_metric__name', 'engagement_metric__description',
                'engagement_metric__engagementmetricconfig__icon_class' ) \
            .filter(questionnaire__targets__id=employee.user.id) \
            .annotate(value=models.Avg('value'))

    return render(request, 'tcc/views/dashboard/profile.html', {
        'profile': employee,
        'inventory': inventory,
        'user_teams': user_teams,
        'skill_list': engagement_metrics,
        'goals': goals,
        'badges': badges
    })


@login_required
def purchase_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    employee = request.user.employee
    purchase = Purchase(product=product, employee=employee)
    try:
        purchase.full_clean()
        purchase.save()
        messages.add_message(request, messages.SUCCESS, _("Item purchased!"))
        messages.add_message(request, messages.WARNING, "<strong><i class=\"fa fa-diamond\"></i> - D$ %d.</strong>" % (product.price))
    except ValidationError as e:
        non_field_errors = e.message_dict[NON_FIELD_ERRORS]
        messages.add_message(request, messages.ERROR, non_field_errors[0])
    finally:
        return redirect(reverse('dashboard'))

@method_decorator(login_required, name='dispatch')
class QuestionnaireView(GenericQuestionnaireView):

    def forms_valid(self, form, inlines):
        update_score_signal.connect(update_money)
        return super(QuestionnaireView, self).forms_valid(form, inlines)


@method_decorator(user_passes_test(lambda u: not u.is_staff), name='dispatch')
class SatisfactionQuestionnaire(QuestionnaireView):

    template_name = 'tcc/views/questionnaire/satisfaction_questionnaire.html'
    form_class = SatisfactionQuestionnaireForm

    def get(self, request):
        if request.user.employee.answered_satisfaction_questionnaire():
            messages.add_message(request, messages.ERROR, _("You have already answered this quiz this week!"))
            return redirect(reverse('dashboard'))

        return super(SatisfactionQuestionnaire, self).get(request)

    def get_initial(self):
        return {
            'targets': self.request.user.id,
            'questionnaire_type': COLLABORATOR_SATISFACTION
        }

    def questions(self):
        return [
            {'question':_('In a scale of 1 to 10, how was your week, considering your sports, meals and relationships?'), 'engagement_metric': 9},
            {'question':_('Considering the amount of work, team mates, noise, how was your week at work?'), 'engagement_metric': 10},
            {'question':_('In a scale of 1 to 10, what is your satisfaction of working with us?'), 'engagement_metric': 11},
        ]

@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class ManagerToCollaboratorQuestionnaire(QuestionnaireView):

    template_name = 'tcc/views/questionnaire/manager_to_collaborator.html'
    form_class = UserQuestionnaireForm

    def get_initial(self):
        return {'targets': self.kwargs['user_id'], 'questionnaire_type': MANAGER_COLLABORATOR}

    def questions(self):
        return [
            {'question':_('How would you rate this member\'s level of communication skills?'), 'engagement_metric': 1},
                    {'question':_('How would you rate the conducted working quality of this member?'), 'engagement_metric': 2},
                    {'question':_('How would you rate the done working speed of this member?'), 'engagement_metric': 3},
                    {'question':_('How would you rate the way this member share responsabilities?'), 'engagement_metric': 4},
                    {'question':_('How would you rate the positiveness of his/her presence?'), 'engagement_metric': 5},
                    {'question':_('How would you rate the satisfaction of others about working with this member?'), 'engagement_metric': 6},
                    {'question':_('How would you rate this member\'s team work?'), 'engagement_metric': 7},
                    {'question':_('How would you rate this member\'s improvement as a whole?'), 'engagement_metric': 8}
        ]

class TaskQuestionnaire(QuestionnaireView):

    template_name = 'tcc/views/questionnaire/task_questionnaire.html'
    form_class = TaskQuestionnaireForm

    def get_initial(self):
        return {'targets': self.kwargs['user_id'], 'questionnaire_type': TASK_FEEDBACK}

    def questions(self):
        return [
            {'question':_('How would you rate the conducted working quality of this task?'), 'engagement_metric': 2},
            {'question':_('How would you rate the done working speed of this task?'), 'engagement_metric': 3},
            {'question':_('How would you rate your overall satisfaction of this task over past works?'), 'engagement_metric': 8}
        ]

class TeamMembersQuestionnaire(PermissionRequiredMixin, FormSetView):
    template_name = 'tcc/views/questionnaire/team_member_questionnaire.html'
    form_class = PeerToPeerQuestionnaireForm
    fields = ['date_of_birth', 'hiring_date']
    extra = 0
    permission_required = 'tcc.receive_peer_feedback_team'

    def get_object(self):
        return Team.objects.get(pk=self.kwargs['team_id'])

    def get_extra_form_kwargs(self):
        kwargs = super(TeamMembersQuestionnaire, self).get_extra_form_kwargs()
        kwargs['engagement_metrics'] = self.engagement_metrics()
        kwargs['team'] = self.kwargs['team_id']
        kwargs['questionnaire_type'] = COLLABORATOR_SATISFACTION
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()
        return super(TeamMembersQuestionnaire, self).dispatch(request, *args, **kwargs)

    def engagement_metrics(self):
        return [1, 2, 3, 4, 5, 6, 7, 8]

    def members(self):
        return Employee.objects \
            .filter(team=self.kwargs['team_id']) \
            .exclude(id=self.request.user.employee.pk)

    def get_initial(self):
        if self.request.method == 'POST':
            return []
        else:
            initial = []
            for member in self.members():
                initial.append({'target': member.id})
            return initial

    def questions(self):
        return [
            _('How would you rate this member\'s level of communication skills?'),
            _('How would you rate the conducted working quality of this member?'),
            _('How would you rate the done working speed of this member?'),
            _('How would you rate the way this member share responsabilities?'),
            _('How would you rate the positiveness of his/her presence?'),
            _('How would you rate the satisfaction of others about working with this member?'),
            _('How would you rate this member\'s team work?'),
            _('How would you rate this member\'s improvement as a whole?')
        ]

    def formset_valid(self, formset):
        messages.add_message(self.request, messages.SUCCESS, _("Thank you for your feedback!"))
        for form in formset:
            questionnaire = form.save()
            update_score(self.request, questionnaire)
            update_money(None, questionnaire, self.request)
        control = TeamQuestionnaireControl(
            employee=self.request.user.employee, team=self.get_object())
        control.save()
        return super(TeamMembersQuestionnaire, self).formset_valid(formset)

class TeamTaskQuestionnaire(TaskQuestionnaire):

    template_name = 'tcc/views/questionnaire/team_task_questionnaire.html'
    form_class = QuestionnaireForm
    inlines = [AnswersInline, TeamQuestionnaireInline]

    def get_initial(self):
        return {'questionnaire_type': TASK_FEEDBACK}

    def construct_inlines(self):
        inline_formsets = super(TeamTaskQuestionnaire, self).construct_inlines()
        return inline_formsets

    def get_form_kwargs(self):
        return super(GenericQuestionnaireView, self).get_form_kwargs()

@login_required
def update_profile(request):
    if request.user.employee.first_login and not request.user.is_superuser:
        form_class = FirstLoginForm
    else:
        form_class = UpdateLoginForm
    if request.method == "POST":
        form = form_class(user=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            message = _("Your profile were updated!")
            messages.add_message(request, messages.SUCCESS, message)
            update_session_auth_hash(request, form.instance)
            return redirect(reverse('dashboard'))
    else:
        form = form_class(user=request.user)

    return render(request, 'tcc/views/dashboard/update_profile.html', {
        'form': form
    });

@login_required
@user_passes_test(lambda u: not u.is_staff)
def shop(request):
    featured_products = Product.objects.featured()
    products = Product.objects.not_featured()
    return render(request, 'tcc/views/shop/index.html', {
        'featured_products': featured_products,
        'products': products,
    });

class TeamDetail(DetailView):
    model = Team
    template_name = 'tcc/views/team/details.html'
