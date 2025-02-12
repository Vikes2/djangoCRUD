import factory
from tenants import models


class TenantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tenant

    name = factory.Faker("name")
    domain = factory.Sequence(lambda x: f"domain{x}")
