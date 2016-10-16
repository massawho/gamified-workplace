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
from .models import (Product, Employee, Purchase, Goal,
    MANAGER_COLLABORATOR, COLLABORATOR_SATISFACTION, TASK_FEEDBACK)
from .questionnaire.forms import AnswersInline
from .questionnaire.models import EngagementMetric, Answer, Questionnaire
from .questionnaire.signals import update_score
from .questionnaire.views import GenericQuestionnaireView
from .forms import (UserQuestionnaireForm, SatisfactionQuestionnaireForm, FirstLoginForm,
                    QuestionnaireForm, UpdateLoginForm, TaskQuestionnaireForm)
from .signals import update_money


@login_required
def dashboard(request):
    if not request.user.is_staff:
        goals = Goal.objects.all()
        badges = request.user.employee.badge_set.all()
        featured_products = Product.objects.filter(is_active=True, is_featured=True)
        inventory = request.user.employee.get_inventory()
        engagement_metrics = Answer.objects \
            .values('engagement_metric', 'engagement_metric__name', 'engagement_metric__description',
                'engagement_metric__engagementmetricconfig__icon_class' ) \
            .filter(questionnaire__targets__id=request.user.pk,
                engagement_metric__engagementmetricconfig__is_staff=False) \
            .annotate(value=models.Avg('value'))

        return render(request, 'tcc/views/dashboard/user_dashboard.html', {
            'profile': request.user,
            'featured_products': featured_products,
            'inventory': inventory,
            'goals': goals,
            'badges': badges,
            'skill_list': engagement_metrics
        })
    else:
        User = get_user_model()
        users = User.objects.filter(is_staff=False)


        return render(request, 'tcc/views/dashboard/manager_dashboard.html', {
            'users': sorted(users, key=lambda user: user.employee.points, reverse=True),
        })


@login_required
@user_passes_test(lambda u: u.is_staff)
def profile(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id, is_staff=False)

    inventory = user.employee.get_inventory()

    goals = Goal.objects.all()
    badges = user.employee.badge_set.all()

    engagement_metrics = Answer.objects \
            .values('engagement_metric', 'engagement_metric__name', 'engagement_metric__description',
                'engagement_metric__engagementmetricconfig__icon_class' ) \
            .filter(questionnaire__targets__id=user.id) \
            .annotate(value=models.Avg('value'))

    return render(request, 'tcc/views/dashboard/profile.html', {
        'profile': user,
        'inventory': inventory,
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
        update_score.connect(update_money)
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
