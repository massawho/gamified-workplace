from django.contrib import messages
from django.dispatch import receiver
from django.db.models import F
from .models import (Employee,
    MANAGER_COLLABORATOR, COLLABORATOR_SATISFACTION, TASK_FEEDBACK)
from .questionnaire.models import Questionnaire
from .questionnaire.signals import update_score

def update_money(sender, instance, request, **kwargs):
    money = 0
    added_money = 0
    users = []
    if instance.questionnaire_type_id is MANAGER_COLLABORATOR or instance.questionnaire_type_id is TASK_FEEDBACK:
        money = int(instance.score)
        users = instance.targets.values_list('id', flat=True)
        if request.user.is_staff:
            money += 10
        else:
            added_money = 10
            Employee.objects.filter(user_id=request.user.pk).update(money=F('money')+added_money)

    elif instance.questionnaire_type_id is COLLABORATOR_SATISFACTION:
        added_money = money = 10
        users = [request.user.pk]

    if added_money is not 0:
        messages.add_message(
            request,
            messages.INFO,
            "<strong><i class=\"fa fa-diamond\"></i> + D$ %d.</strong>" % (added_money)
        )

    Employee.objects.filter(user_id__in=users).update(money=F('money')+money)
