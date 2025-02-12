from multitenancy import fields as multitenancy_fields
from multitenancy import models as multitenancy_models
from rest_framework import fields, serializers
from tenants import models as tenant_models


class ModelWithTenantSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=fields.empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        if data is not fields.empty and isinstance(data, dict):
            self.initial_data["tenant"] = self.tenant_id

    def build_relational_field(self, field_name, relation_info):
        field_class, field_kwargs = super().build_relational_field(
            field_name, relation_info
        )
        if issubclass(relation_info.related_model, multitenancy_models.TenantModel):
            field_class = multitenancy_fields.TenantPrimaryKeyRelatedField
        return field_class, field_kwargs

    @property
    def tenant_id(self):
        return self.context["tenant_id"]

    @property
    def tenant(self):
        return tenant_models.Tenant.objects.get(pk=self.tenant_id)

    @property
    def validated_data(self):
        validated_data = super().validated_data
        validated_data["tenant"] = self.tenant
        return validated_data
