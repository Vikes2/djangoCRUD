import factory
from departments import models
from organizations.tests import factories as organizations_factories
from tenants.tests import factories as tenant_factories


class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Departament

    name = factory.Sequence(lambda x: f"department_name{x}")
    organization = factory.SubFactory(organizations_factories.OrganizationFactory)
    tenant = factory.SubFactory(tenant_factories.TenantFactory)
