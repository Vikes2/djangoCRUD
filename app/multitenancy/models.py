from django.db import models
from multitenancy.querysets import TenantQuerySet
from tenants.models import Tenant


class TenantModel(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.PROTECT, related_name="%(class)ss"
    )

    objects = TenantQuerySet.as_manager()

    class Meta:
        abstract = True
