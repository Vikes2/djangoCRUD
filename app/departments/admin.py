from customers.models import Customer
from departments.models import Departament
from django.contrib import admin


class CustomerInline(admin.TabularInline):
    model = Customer


class DepartamentAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "id",
    ]
    inlines = [
        CustomerInline,
    ]


admin.site.register(Departament, DepartamentAdmin)
