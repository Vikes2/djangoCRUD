from multitenancy.mixins import TenantViewMixin
from organizations import models
from organizations.serializers import OrganizationSerializer
from rest_framework import viewsets


# ViewSets define the view behavior.
class OrganizationViewSet(TenantViewMixin, viewsets.ModelViewSet):
    queryset = models.Organization.objects.all()
    serializer_class = OrganizationSerializer
