from datetime import datetime
from django.db import models
from datetime import timedelta


class EmployeeManager(models.Manager):

    def decrease_energy(self, user):
        return self.filter(user_id=user.pk).update(energy=models.F('energy')-1)

    def add_money_to_user(self, user, money):
        return self.filter(user_id=user.pk).update(money=models.F('money')+money)

    def add_money_to_users(self, users, money):
        return self.filter(user_id__in=users).update(money=models.F('money')+money)

    def managers(self):
        return self.filter(user__is_staff=True)

    def collaborators(self):
        return self.filter(user__is_staff=False, is_guest=False)


class TeamManager(models.Manager):

    def active(self):
        return self.filter(ended_at__isnull=True)

    def inactive(self):
        return self.filter(ended_at__isnull=False)


class ProductManager(models.Manager):

    def active(self):
        return self.filter(is_active=True)

    def featured(self):
        return self.active().filter(is_featured=True)

    def not_featured(self):
        return self.active().filter(is_featured=False)


class GoalManager(models.Manager):

    def not_taken(self, employee):
        today = datetime.today()
        beginning_of_week = datetime.today() - timedelta(
            days=today.isoweekday() % 7
        )
        beginning_of_month = today.replace(day=1)

        return self.raw(
            '''
                SELECT DISTINCT "tcc_goal"."id", "tcc_goal"."description",
                    "tcc_goal"."money", "tcc_goal"."frequency",
                    "tcc_goal"."starts_at", "tcc_goal"."ends_at",
                    "tcc_goal"."level", "tcc_goal"."is_active"
                FROM "tcc_goal"
                LEFT JOIN "tcc_badge"
                    ON (
                        "tcc_goal"."id" = "tcc_badge"."goal_id"
                        AND "tcc_badge"."employee_id" != %d
                        AND CASE
                            WHEN "tcc_goal"."frequency" = 2 THEN "tcc_badge"."received_at" >= '%s'
                            WHEN "tcc_goal"."frequency" = 3 THEN "tcc_badge"."received_at" >= '%s'
                            WHEN "tcc_goal"."frequency" = 4 THEN "tcc_badge"."received_at" >= '%s'
                        END
                    )
                WHERE "tcc_badge"."id" IS NULL
                AND '%s' BETWEEN
                    "tcc_goal"."starts_at"
                    AND "tcc_goal"."ends_at"
            ''' % (
            employee.id,
            today,
            beginning_of_week,
            beginning_of_month,
            today
            )
        )
