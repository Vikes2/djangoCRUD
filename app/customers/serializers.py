# Create your views here.
from customers import models
from multitenancy import serializers as multitenancy_serializers


class CustomerSerializer(multitenancy_serializers.ModelWithTenantSerializer):
    class Meta:
        model = models.Customer
        fields = ["id", "name", "department"]
