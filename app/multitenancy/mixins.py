from django.shortcuts import get_object_or_404
from tenants import models as tenant_models


class TenantViewMixin:
    @property
    def tenant_id(self):
        tenant_name = self.request.headers.get("X-TENANT")
        tenant = get_object_or_404(tenant_models.Tenant, name=tenant_name)
        return tenant.pk

    def get_queryset(self):
        return super().get_queryset().with_tenant(self.tenant_id)

    # TODO: verify if needed, propably in update?
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["tenant_id"] = self.tenant_id
        return context
