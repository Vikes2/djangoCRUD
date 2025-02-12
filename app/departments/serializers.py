# Create your views here.
from departments import models
from multitenancy import serializers as multitenancy_serializers


class DepartmentSerializer(multitenancy_serializers.ModelWithTenantSerializer):
    class Meta:
        model = models.Departament
        fields = ["id", "name", "organization"]
