from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from apps.tcc.forms import EmployeeFormSet
from apps.tcc.models import Employee, Department, Occupation, Product, Team
from apps.utils.filters import IsNullFieldListFilter
from django.utils.translation import ugettext_lazy as _


class DepartmentFilter(admin.SimpleListFilter):
    """This is a list filter based on the values
    from a model's `keywords` ArrayField. """

    title = 'Departments'
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

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Occupation, OccupationAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Team, TeamAdmin)
