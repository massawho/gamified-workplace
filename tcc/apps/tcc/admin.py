from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from apps.utils.filters import IsNullFieldListFilter
from django.utils.translation import ugettext_lazy as _
from .forms import EmployeeFormSet, EngagementMetricConfigFormSet
from .models import Employee, Department, Occupation, Product, Team, EngagementMetricConfig
from .questionnaire.admin import EngagementMetricAdmin as BaseEngagementMetricAdmin
from .questionnaire.models import EngagementMetric


class DepartmentFilter(admin.SimpleListFilter):
    """This is a list filter based on the values
    from a model's `keywords` ArrayField. """

    title = _('Departments')
    parameter_name = 'department'

    def lookups(self, request, model_admin):
        # Very similar to our code above, but this method must return a
        # list of tuples: (lookup_value, human-readable value). These
        # appear in the admin's right sidebar

        departments = Department.objects.all()
        return [(department.id, department.name) for department in departments]

    def queryset(self, request, queryset):
        # when a user clicks on a filter, this method gets called. The
        # provided queryset with be a queryset of Items, so we need to
        # filter that based on the clicked keyword.

        lookup_value = self.value()  # The clicked keyword. It can be None!
        if lookup_value:
            # the __contains lookup expects a list, so...
            queryset = queryset.filter(employee__department_id=lookup_value)
        return queryset

class DepartmentAdmin(admin.ModelAdmin):
    model = Department

class OccupationAdmin(admin.ModelAdmin):
    model = Occupation

class TeamAdmin(admin.ModelAdmin):
    model = Team
    list_display = ('name', 'is_active', 'ended_at')
    list_filter = (('ended_at', IsNullFieldListFilter), 'members',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "members":
            kwargs["queryset"] = Employee.objects.filter(user__is_staff=False)
        return super(TeamAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('name', 'is_active', 'is_featured', 'price', 'stock')
    list_filter = ('is_active', 'is_featured')

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'
    formset = EmployeeFormSet

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline, )
    list_filter = (DepartmentFilter, 'is_active', 'is_staff', 'is_superuser')

# Define an inline admin descriptor for EngagementMetricConfig model
# which acts a bit like a singleton
class EngagementMetricConfigInline(admin.StackedInline):
    model = EngagementMetricConfig
    can_delete = False
    verbose_name_plural = 'engagement_metric'
    formset = EngagementMetricConfigFormSet

class EngagementMetricAdmin(BaseEngagementMetricAdmin):
    inlines = (EngagementMetricConfigInline, )
    list_display = ['name', 'description', 'get_is_staff']
    list_filter = ('engagementmetricconfig__is_staff', )

    def get_is_staff(self, obj):
        return obj.engagementmetricconfig.is_staff
    get_is_staff.admin_order_field  = 'engagementmetricconfig__is_staff'  #Allows column order sorting
    get_is_staff.short_description = _('Displayed only for staff')  #Renames column head
    get_is_staff.boolean = True

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# Re-register EngagementMetricAdmin
admin.site.unregister(EngagementMetric)
admin.site.register(EngagementMetric, EngagementMetricAdmin)

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Occupation, OccupationAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Team, TeamAdmin)
