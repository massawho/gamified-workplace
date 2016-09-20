from django.contrib import admin
from .models import EngagementMetric

class EngagementMetricAdmin(admin.ModelAdmin):
    model = EngagementMetric
    list_display = ('name', 'description')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_create_permission(self, request, obj=None):
        return False

admin.site.register(EngagementMetric, EngagementMetricAdmin)
