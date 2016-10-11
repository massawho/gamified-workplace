from django.db import models


class EmployeeManager(models.Manager):

    def add_money_to_user(self, user, money):
        return self.filter(user_id=user.pk).update(money=models.F('money')+money)

    def add_money_to_users(self, users, money):
        return self.filter(user_id__in=users).update(money=models.F('money')+money)


class ProductManager(models.Manager):

    def active(self):
        return self.filter(is_active=True)

    def featured(self):
        return self.active().filter(is_featured=True)

    def not_featured(self):
        return self.active().filter(is_featured=False)
