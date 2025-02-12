import uuid

from django.db import models


class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)  # TODO add unique i guess
    domain = models.CharField(max_length=128)

    def __str__(self):
        return self.name
