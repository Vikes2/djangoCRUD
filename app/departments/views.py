from departments import models
from departments.serializers import DepartmentSerializer
from multitenancy.mixins import TenantViewMixin
from rest_framework import viewsets


# ViewSets define the view behavior.
class DepartmentViewSet(TenantViewMixin, viewsets.ModelViewSet):
    queryset = models.Departament.objects.all()
    serializer_class = DepartmentSerializer
    filterset_fields = ["organization"]
