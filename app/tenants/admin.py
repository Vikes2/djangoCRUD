from django.contrib import admin
from tenants.models import Tenant


class TenantAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "domain",
        "id",
    ]


admin.site.register(Tenant, TenantAdmin)
