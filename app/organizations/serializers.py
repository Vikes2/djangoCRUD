# Create your views here.
from multitenancy import serializers as multitenancy_serializers
from organizations import models


class OrganizationSerializer(multitenancy_serializers.ModelWithTenantSerializer):
    class Meta:
        model = models.Organization
        fields = ["id", "name"]
