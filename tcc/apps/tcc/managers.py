from django.db import models


class ProductManager(models.Manager):

    def active(self):
        return self.filter(is_active=True)

    def featured(self):
        return self.active().filter(is_featured=True)

    def not_featured(self):
        return self.active().filter(is_featured=False)
