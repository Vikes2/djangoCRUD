import uuid

from departments.models import Departament
from django.db import models
from multitenancy import models as multitenancy_models


class Customer(multitenancy_models.TenantModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Departament, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
