from customers.models import Customer
from django.contrib import admin


class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "id",
    ]


admin.site.register(Customer, CustomerAdmin)
