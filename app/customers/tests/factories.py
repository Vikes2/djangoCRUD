import factory
from customers import models
from departments.tests import factories as departments_factories
from tenants.tests import factories as tenant_factories


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Customer

    name = factory.Sequence(lambda x: f"department_name{x}")
    department = factory.SubFactory(departments_factories.DepartmentFactory)
    tenant = factory.SubFactory(tenant_factories.TenantFactory)
