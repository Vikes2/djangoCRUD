from django.apps import apps
from django.db import models
from tenants.models import Tenant


class TenantQuerySet(models.QuerySet):
    tenant_model = Tenant
    tenant_id_field = "tenant__id"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self.tenant_model, str):
            app, model = self.tenant_model.split(".")
            self.tenant_model = apps.get_model(app, model)

    def with_tenant(self, tenant):
        if isinstance(tenant, self.tenant_model):
            tenant_id = tenant.pk
        else:
            tenant_id = tenant
        if tenant_id:
            assert (
                self.query.can_filter()
            ), "Cannot filter a query once a slice has been taken."
            clone = self.filter(**{self.tenant_id_field: tenant_id})
            return clone
        else:
            return self.none()
