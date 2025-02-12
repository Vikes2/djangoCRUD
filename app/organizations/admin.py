from departments.models import Departament
from django.contrib import admin
from organizations.models import Organization


class DepartmentInline(admin.TabularInline):
    model = Departament


class OrganizationAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "id",
    ]
    inlines = [
        DepartmentInline,
    ]


admin.site.register(Organization, OrganizationAdmin)
