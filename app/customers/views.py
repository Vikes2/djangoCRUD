from customers import models
from customers.serializers import CustomerSerializer
from multitenancy.mixins import TenantViewMixin
from rest_framework import viewsets


# ViewSets define the view behavior.
class CustomerViewSet(TenantViewMixin, viewsets.ModelViewSet):
    queryset = models.Customer.objects.all()
    serializer_class = CustomerSerializer
    filterset_fields = ["department"]
