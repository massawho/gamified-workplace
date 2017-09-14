from datetime import date
from dateutil.rrule import rrule, DAILY
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    update_session_auth_hash
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import models
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import (
    check_for_language,
    LANGUAGE_SESSION_KEY,
    ugettext_lazy as _
)
from django.views.generic import DetailView
from extra_views import FormSetView
from rules.contrib.views import PermissionRequiredMixin
from .forms import (
    FirstLoginForm,
    PeerToPeerQuestionnaireForm,
    QuestionnaireForm,
    SatisfactionQuestionnaireForm,
    TaskQuestionnaireForm,
    TeamQuestionnaireInline,
    UpdateLoginForm,
    UserQuestionnaireForm
)
from .models import (
    Employee,
    Goal,
    Product,
    Purchase,
    Team,
    TeamQuestionnaireControl
)
from .signals import update_money
from .questionnaire.forms import AnswersInline
from .questionnaire.models import (
    Answer,
    EngagementMetric,
    Questionnaire,
    QuestionnaireTemplate,
    update_score
)
from .questionnaire.signals import update_score as update_score_signal
from .questionnaire.views import (
    GenericQuestionnaireView,
    QuestionnaireTemplateMixin
)


@login_required
def set_language(request):
    response = HttpResponseRedirect('/')
    if request.method == 'GET':
        lang_code = request.GET.get('language', None)
        if lang_code and check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session[LANGUAGE_SESSION_KEY] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response


@login_required
def dashboard(request):
    if not request.user.is_staff and not request.user.employee.is_guest:
        energy = request.user.employee.reset_energy()
        if energy:
            messages.add_message(
                request,
                messages.INFO,
                "<strong><i class=\"fa fa-bolt\"></i> + 3"
            )

        goals = Goal.objects.not_taken(request.user.employee)
        badges = request.user.employee.badge_set.all()
        featured_products = Product.objects.filter(is_active=True, is_featured=True)
        user_teams = request.user.employee.team_set.active()
        inventory = request.user.employee.get_inventory()
        engagement_metrics = Answer.objects \
            .values(
                'engagement_metric',
                'engagement_metric__name',
                'engagement_metric__description',
                'engagement_metric__engagementmetricconfig__icon_class'
            ) \
            .filter(
                questionnaire__targets__id=request.user.pk,
                engagement_metric__engagementmetricconfig__is_staff=False
            ) \
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
        employees = Employee.objects.collaborators()

        teams = Team.objects.filter(ended_at=None)

        return render(request, 'tcc/views/dashboard/manager_dashboard.html', {
            'employees': sorted(employees, key=lambda employee: employee.points, reverse=True),
            'teams': teams,
        })


@login_required
def collaborator_list(request):
    collaborators = Employee.objects.collaborators()
    return render(request, 'tcc/views/collaborator/list.html', {
        'collaborators': collaborators,
    })


@login_required
def team_list(request):
    active_teams = Team.objects.active()
    inactive_teams = Team.objects.inactive()
    return render(request, 'tcc/views/team/list.html', {
        'active_teams': active_teams,
        'inactive_teams': inactive_teams
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def profile(request, pk):
    employee = get_object_or_404(Employee, pk=pk, user__is_staff=False)

    user_teams = employee.team_set.active()
    inventory = employee.get_inventory()

    goals = Goal.objects.not_taken(employee)
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
@user_passes_test(lambda u: not u.is_staff and not u.employee.is_guest)
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

    def get_initial(self):
        initial = super(QuestionnaireView, self).get_initial()
        initial.update({'targets': self.kwargs['user_id']})
        return initial


@method_decorator(
    user_passes_test(lambda u: not u.is_staff),
    name='dispatch'
)
class SatisfactionQuestionnaire(QuestionnaireView):

    template_name = 'tcc/views/questionnaire/satisfaction_questionnaire.html'
    form_class = SatisfactionQuestionnaireForm

    def get_questionnaire(self):
        return QuestionnaireTemplate.objects.get(pk=1)

    def get(self, request):
        if request.user.employee.answered_satisfaction_questionnaire():
            messages.add_message(request, messages.ERROR, _("You have already answered this quiz this week!"))
            return redirect(reverse('dashboard'))

        return super(SatisfactionQuestionnaire, self).get(request)

    def get_initial(self):
        initial = super(QuestionnaireView, self).get_initial()
        initial.update({'targets': self.request.user.id})
        return initial


@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class ManagerToCollaboratorQuestionnaire(QuestionnaireView):

    template_name = 'tcc/views/questionnaire/manager_to_collaborator.html'
    form_class = UserQuestionnaireForm

    def get_questionnaire(self):
        return QuestionnaireTemplate.objects.get(pk=3)


class TaskQuestionnaire(PermissionRequiredMixin, QuestionnaireView):

    template_name = 'tcc/views/questionnaire/task_questionnaire.html'
    form_class = TaskQuestionnaireForm
    permission_required = 'tcc.receive_task_feedback_employee'

    def get_questionnaire(self):
        return QuestionnaireTemplate.objects.get(pk=2)


class TeamMembersQuestionnaire(PermissionRequiredMixin, QuestionnaireTemplateMixin,
    FormSetView):
    template_name = 'tcc/views/questionnaire/team_member_questionnaire.html'
    form_class = PeerToPeerQuestionnaireForm
    fields = ['date_of_birth', 'hiring_date']
    extra = 0
    permission_required = 'tcc.receive_peer_feedback_team'

    def get_object(self):
        return Team.objects.get(pk=self.kwargs['team_id'])

    def get_questionnaire(self):
        return QuestionnaireTemplate.objects.get(pk=4)

    def get_extra_form_kwargs(self):
        kwargs = super(TeamMembersQuestionnaire, self).get_extra_form_kwargs()
        kwargs['engagement_metrics'] = self.get_engagement_values_list()
        kwargs['team'] = self.kwargs['team_id']
        kwargs['questionnaire_type'] = self.get_questionnaire_type()
        return kwargs

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
    permission_required = 'tcc.receive_task_feedback_team'

    def get_initial(self):
        return super(TaskQuestionnaire, self).get_initial()

    def construct_inlines(self):
        inline_formsets = super(TeamTaskQuestionnaire, self).construct_inlines()
        return inline_formsets

    def get_form_kwargs(self):
        return super(GenericQuestionnaireView, self).get_form_kwargs()

    def get_initial(self):
        return super(QuestionnaireView, self).get_initial()


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
@user_passes_test(lambda u: not u.is_staff and not u.employee.is_guest)
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


@login_required
@user_passes_test(lambda u: u.is_staff)
def collaborator_report(request):
    collaborators = Employee.objects.collaborators()
    metrics = EngagementMetric.objects.all()
    return render(request, 'tcc/views/reports/collaborator.html', {
        'collaborators': collaborators,
        'metrics': metrics
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def overall_average_over_time(request):
    today = date.today()
    start_date = date(today.year-1, today.month, today.day)
    teste = []
    for dt in rrule(DAILY, dtstart=start_date, until=today):
        avg = models.Avg('answer__value')
        t = Questionnaire.objects \
            .filter(created_at__range=(start_date, dt)) \

        if 'collaborator' in request.GET:
            t = t.filter(targets__id=request.GET['collaborator'])

        if 'engagement_metric' in request.GET:
            t = t.filter(answer__engagement_metric=request.GET['engagement_metric'])

        t = t.aggregate(avg=avg)
        if t['avg']:
            teste.append([int(dt.strftime("%s"))*1000, t['avg']])

    return JsonResponse(teste, safe=False)
