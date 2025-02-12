import uuid

from django.db import models
from multitenancy import models as multitenancy_models


class Organization(multitenancy_models.TenantModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
