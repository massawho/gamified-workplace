from django.contrib import admin
from .models import EngagementMetric, QuestionnaireTemplate, QuestionTemplate


class QuestionTemplateAdmin(admin.ModelAdmin):
    model = QuestionTemplate
    list_display = ('question', 'engagement_metric')

class QuestionnaireTemplateAdmin(admin.ModelAdmin):
    model = QuestionnaireTemplate
    list_display = ('description', 'questionnaire_type', 'id')
    filter_horizontal = ('questions',)

class EngagementMetricAdmin(admin.ModelAdmin):
    model = EngagementMetric
    list_display = ('name', 'description')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_create_permission(self, request, obj=None):
        return False

admin.site.register(EngagementMetric, EngagementMetricAdmin)
admin.site.register(QuestionTemplate, QuestionTemplateAdmin)
admin.site.register(QuestionnaireTemplate, QuestionnaireTemplateAdmin)
