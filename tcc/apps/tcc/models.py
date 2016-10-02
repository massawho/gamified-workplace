from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from .questionnaire.models import EngagementMetric
from datetime import datetime, timedelta


MANAGER_COLLABORATOR = 1
COLLABORATOR_SATISFACTION = 2
TASK_FEEDBACK = 3


class Department(models.Model):
    name = models.CharField(
        max_length=25
    )

    def __str__(self):
        return self.name


class Occupation(models.Model):
    name = models.CharField(
        max_length=25
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        _('Product name'),
        max_length=45
    )
    price = models.PositiveIntegerField(
        _('Price'),
        help_text=_('Cost in points')
    )
    stock = models.IntegerField(
        _('Stock'),
        default=-1,
        help_text=_('-1 means unlimited stock')
    )
    max_per_user = models.PositiveIntegerField(
        _('Max purchases per user'),
        default=0,
        help_text=_('0 means no limit')
    )
    is_active = models.BooleanField(
        default = True
    )
    is_featured = models.BooleanField()

    def relevant_stock(self):
        if self.max_per_user > 0:
            return self.max_per_user
        elif self.stock > -1:
            return self.stock
        else:
            return -1

    def __str__(self):
        return self.name


GOAL_LEVELS = (
    (4, _('Platinum')),
    (3, _('Gold')),
    (2, _('Silver')),
    (1, _('Bronze'))
)


class Goal(models.Model):
    description = models.CharField(
        max_length=40,
        help_text=_('A short name to describe the goal')
    )
    money = models.PositiveIntegerField(
        _('Diamonds'),
        default=0,
        help_text=_('Diamonds received when employee finishes this goal')
    )
    level = models.PositiveIntegerField(
        choices=GOAL_LEVELS,
        default=1,
        help_text=_('The level of importance of this goal'),
    )
    is_active = models.BooleanField(
        default = True
    )
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.description


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    occupation = models.ForeignKey(Occupation, on_delete=models.PROTECT, null=True)
    nickname = models.CharField(
        max_length=25,
        null=True,
        blank=True,
    )
    hiring_date = models.DateField(
        null=True,
        blank=False,
    )
    date_of_birth = models.DateField(
        null=True,
        blank=False,
    )
    money = models.PositiveIntegerField(
        editable=False,
        default=0
    )
    inventory = models.ManyToManyField(Product, through='Purchase')
    badges = models.ManyToManyField(Goal, through='Badge')

    def __str__(self):
        return self.nickname or self.user.get_short_name() or self.user.username

    @cached_property
    def points(self):
        points_calc = models.Sum('answer__value')
        points = self.user.questionnaire_set \
            .exclude(questionnaire_type__in=[COLLABORATOR_SATISFACTION]) \
            .aggregate(points=points_calc)['points'] or 0
        return int(points/10)

    def answered_satisfaction_questionnaire(self):
        last_week = datetime.today() + timedelta(days=-7)
        return self.user.questionnaire_set \
            .filter(questionnaire_type=COLLABORATOR_SATISFACTION, created_at__gte=last_week) \
            .exists()

    @property
    def feedbacks(self):
        return self.user.questionnaire_set \
            .exclude(questionnaire_type__in=[COLLABORATOR_SATISFACTION]) \
            .count()

    @cached_property
    def overall_skill_bar(self):
        skill_calc = models.Avg('answer__value')
        return self.user.questionnaire_set.aggregate(skill_bar=skill_calc)['skill_bar'] or 0


class Badge(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    received_at = models.DateField(
        null=True,
        blank=True
    )


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    cost = models.PositiveIntegerField(
        editable=False,
        null=False,
        blank=True,
    )
    used_at = models.DateField(
        null=True,
        blank=True,
        editable=False
    )
    purchase_date = models.DateField(
        auto_now=True,
        editable=False
    )

    def clean(self):
        if self.employee.money < self.product.price:
            raise ValidationError(_('You don\'t have enough money.'))

        if self.product.stock == 0 or not self.product.is_active:
            raise ValidationError(_('This item is not available.'))

        count_product = self.employee.inventory.filter(id=self.product.id).count()
        if self.product.max_per_user > 0 and count_product >= self.product.max_per_user:
            raise ValidationError(_('You already own this product.'))

        if self.cost is None:
            self.cost = self.product.price


class Team(models.Model):
    name = models.CharField(
        max_length=25
    )
    members = models.ManyToManyField(Employee)
    created_at = models.DateField()
    ended_at = models.DateField(
        null=True,
        blank=True
    )

    def is_active(self):
        return self.ended_at == None

    def __str__(self):
        return self.name


class EngagementMetricConfig(models.Model):
    engagement_metric = models.OneToOneField(
        EngagementMetric,
        on_delete=models.CASCADE,
        primary_key=True
    )
    icon_class = models.CharField(
        _('Icon class'),
        max_length=25,
        help_text=_('An icon class (eg: fontawesome) to be displayed.')
    )
    is_staff = models.BooleanField(
        _('Displayed only for staff'),
        default=False,
        help_text=_('Should this metric be displayed only by staff?')
    )

@receiver(post_save, sender=Purchase)
def update_data_after_purchase(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        if product.stock > 0:
            product.stock -= 1
            product.save()

        employee = instance.employee
        employee.money -= instance.cost
        employee.save()
