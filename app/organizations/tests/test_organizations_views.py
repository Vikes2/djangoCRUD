import pytest
from organizations import models
from organizations.tests import factories
from rest_framework import status
from rest_framework.authtoken.models import Token
from tenants.tests import factories as tenants_factories
from utils.tests import factories as utils_factories


@pytest.mark.django_db
def test_organization_view_unauthorized(client):
    organization = factories.OrganizationFactory()
    response = client.get(
        f"/organizations/{organization.id}/",
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_organization_view_no_tenant(client):
    organization = factories.OrganizationFactory()
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.get(
        f"/organizations/{organization.id}/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_organization_retreive_view(client):
    tenant = tenants_factories.TenantFactory(name="my_tenant_name")
    organization = factories.OrganizationFactory(tenant=tenant)
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.get(
        f"/organizations/{organization.id}/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=tenant.name,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": str(organization.id), "name": organization.name}


@pytest.mark.django_db
def test_organization_list_view(client):
    tenant = tenants_factories.TenantFactory(name="my_tenant_name")
    organization1 = factories.OrganizationFactory(tenant=tenant)
    organization2 = factories.OrganizationFactory(tenant=tenant)
    (factories.OrganizationFactory())  # organization3 has different tenant
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.get(
        "/organizations/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=tenant.name,
    )
    assert response.status_code == status.HTTP_200_OK
    resp = response.json()
    assert len(resp) == 2
    assert resp == [
        {
            "id": str(organization1.id),
            "name": organization1.name,
        },
        {
            "id": str(organization2.id),
            "name": organization2.name,
        },
    ]


@pytest.mark.django_db
def test_organization_delete_view_no_tenant(client):
    tenant = tenants_factories.TenantFactory(name="my_tenant_name")
    organization1 = factories.OrganizationFactory(tenant=tenant)
    assert models.Organization.objects.count() == 1
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.delete(
        f"/organizations/{organization1.id}/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_organization_delete_view(client):
    tenant = tenants_factories.TenantFactory(name="my_tenant_name")
    organization1 = factories.OrganizationFactory(tenant=tenant)
    assert models.Organization.objects.count() == 1
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.delete(
        f"/organizations/{organization1.id}/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=tenant.name,
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert models.Organization.objects.count() == 0


@pytest.mark.django_db
def test_organization_delete_view_different_tenant(client):
    tenant = tenants_factories.TenantFactory(name="diff_tenant")
    organization1 = factories.OrganizationFactory()
    assert models.Organization.objects.count() == 1
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.delete(
        f"/organizations/{organization1.id}/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=tenant.name,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_organization_create_view(client):
    tenant = tenants_factories.TenantFactory(name="my_tenant_name")
    data = {
        "name": "organization_name",
    }
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)
    response = client.post(
        "/organizations/",
        data=data,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=tenant.name,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert models.Organization.objects.filter(tenant=tenant).count() == 1


@pytest.mark.django_db
def test_organization_update_view(client):
    tenant = tenants_factories.TenantFactory(name="my_tenant_name")
    organization = factories.OrganizationFactory(name="org_name_old", tenant=tenant)
    data = {
        "name": "org_name_new",
    }
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)
    response = client.put(
        f"/organizations/{organization.id}/",
        data=data,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=tenant.name,
    )
    assert response.status_code == status.HTTP_200_OK
    organization.refresh_from_db()
    assert organization.name == "org_name_new"
