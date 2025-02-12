import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token
from tenants import models
from tenants.tests import factories
from utils.tests import factories as utils_factories


@pytest.mark.django_db
def test_tenant_retreive_view_unauthorized(client):
    tenant = factories.TenantFactory()
    response = client.get(
        f"/tenants/{tenant.id}/",
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_tenant_retreive_view(client):
    tenant = factories.TenantFactory()
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.get(
        f"/tenants/{tenant.id}/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
    )
    assert response.status_code == status.HTTP_200_OK
    resp = response.json()
    assert resp == {
        "id": f"{tenant.id}",
        "domain": f"{tenant.domain}",
        "name": f"{tenant.name}",
    }


@pytest.mark.django_db
def test_tenant_list_view(client):
    tenant1 = factories.TenantFactory()
    tenant2 = factories.TenantFactory()
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.get(
        "/tenants/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
    )
    assert response.status_code == status.HTTP_200_OK
    resp = response.json()
    assert len(resp) == 2
    assert resp == [
        {
            "id": f"{tenant1.id}",
            "domain": f"{tenant1.domain}",
            "name": f"{tenant1.name}",
        },
        {
            "id": f"{tenant2.id}",
            "domain": f"{tenant2.domain}",
            "name": f"{tenant2.name}",
        },
    ]


@pytest.mark.django_db
def test_tenant_delete_view(client):
    tenant = factories.TenantFactory()
    assert models.Tenant.objects.count() == 1
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.delete(
        f"/tenants/{tenant.id}/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert models.Tenant.objects.count() == 0


@pytest.mark.django_db
def test_tenant_create_view(client):
    data = {
        "name": "tenant_name",
        "domain": "tenant_domain",
    }
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)
    response = client.post(
        "/tenants/",
        data=data,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert models.Tenant.objects.count() == 1


@pytest.mark.django_db
def test_tenant_update_view(client):
    tenant = factories.TenantFactory(name="name_old", domain="domain_old")
    data = {
        "name": "name_new",
        "domain": "domain_new",
    }
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)
    response = client.put(
        f"/tenants/{tenant.id}/",
        data=data,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
    )
    assert response.status_code == status.HTTP_200_OK
    tenant.refresh_from_db()
    assert tenant.name == "name_new"
    assert tenant.domain == "domain_new"
