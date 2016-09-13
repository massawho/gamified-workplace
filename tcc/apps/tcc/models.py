from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(
        max_length=25
    )

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    nickname = models.CharField(
        max_length=25,
        null=True,
        blank=True,
    )
    date_of_birth = models.DateField(
        null=True,
        blank=False,
    )

    def __str__(self):
        return self.nickname
