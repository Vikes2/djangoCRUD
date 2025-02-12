import factory
from organizations import models
from tenants.tests import factories as tenant_factories


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Organization

    name = factory.Sequence(lambda x: f"org_name{x}")
    tenant = factory.SubFactory(tenant_factories.TenantFactory)
