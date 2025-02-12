import uuid

from django.db import models
from multitenancy import models as multitenancy_models
from organizations.models import Organization


class Departament(multitenancy_models.TenantModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
