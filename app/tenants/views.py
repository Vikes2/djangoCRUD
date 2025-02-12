from rest_framework import viewsets
from tenants import models, serializers


# Create your views here.
class TenantViewset(viewsets.ModelViewSet):
    queryset = models.Tenant.objects.all()
    serializer_class = serializers.TenantSerializer
    # permission_classes = [clms_permissions.IsAdmin]
