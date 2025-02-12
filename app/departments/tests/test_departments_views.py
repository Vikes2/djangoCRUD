from unittest.mock import ANY

import pytest
from departments import models
from departments.tests import factories
from organizations.tests import factories as organizations_factories
from rest_framework import status
from rest_framework.authtoken.models import Token
from tenants.tests import factories as tenants_factories
from utils.tests import factories as utils_factories


@pytest.mark.django_db
def test_department_view_unauthorized(client):
    department = factories.DepartmentFactory()
    response = client.get(
        f"/departments/{department.id}/",
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_department_view_no_tenant(client):
    department = factories.DepartmentFactory()
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.get(
        f"/departments/{department.id}/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_department_retreive_view(client):
    tenant = tenants_factories.TenantFactory(name="my_tenant_name")
    department = factories.DepartmentFactory(tenant=tenant)
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.get(
        f"/departments/{department.id}/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=tenant.name,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": str(department.id),
        "name": department.name,
        "organization": str(department.organization.id),
    }


@pytest.mark.django_db
def test_department_list_view(client):
    tenant = tenants_factories.TenantFactory(name="my_tenant_name")
    department1 = factories.DepartmentFactory(tenant=tenant)
    department2 = factories.DepartmentFactory(tenant=tenant)
    factories.DepartmentFactory()  # department3 has different tenant
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.get(
        "/departments/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=tenant.name,
    )
    assert response.status_code == status.HTTP_200_OK
    resp = response.json()
    assert len(resp) == 2
    assert resp == [
        {
            "id": str(department1.id),
            "name": department1.name,
            "organization": str(department1.organization.id),
        },
        {
            "id": str(department2.id),
            "name": department2.name,
            "organization": str(department2.organization.id),
        },
    ]


@pytest.mark.django_db
def test_department_list_view_organization_filter(client):
    tenant = tenants_factories.TenantFactory(name="my_tenant_name")
    organization = organizations_factories.OrganizationFactory()
    department1 = factories.DepartmentFactory(tenant=tenant, organization=organization)
    department2 = factories.DepartmentFactory(tenant=tenant, organization=organization)
    factories.DepartmentFactory(tenant=tenant)  # department4 has different organization
    factories.DepartmentFactory()  # department4 has different tenant
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.get(
        f"/departments/?organization={organization.id}",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=tenant.name,
    )
    assert response.status_code == status.HTTP_200_OK
    resp = response.json()
    assert len(resp) == 2
    assert resp == [
        {
            "id": str(department1.id),
            "name": department1.name,
            "organization": str(department1.organization.id),
        },
        {
            "id": str(department2.id),
            "name": department2.name,
            "organization": str(department2.organization.id),
        },
    ]


@pytest.mark.django_db
def test_department_delete_view_no_tenant(client):
    department1 = factories.DepartmentFactory()
    assert models.Departament.objects.count() == 1
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.delete(
        f"/departments/{department1.id}/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_department_delete_view(client):
    tenant = tenants_factories.TenantFactory(name="my_tenant_name")
    department1 = factories.DepartmentFactory(tenant=tenant)
    assert models.Departament.objects.count() == 1
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.delete(
        f"/departments/{department1.id}/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=tenant.name,
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert models.Departament.objects.count() == 0


@pytest.mark.django_db
def test_department_delete_view_different_tenant(client):
    tenant = tenants_factories.TenantFactory(name="diff_tenant")
    department1 = factories.DepartmentFactory()
    assert models.Departament.objects.count() == 1
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.delete(
        f"/departments/{department1.id}/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=tenant.name,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert models.Departament.objects.count() == 1


@pytest.mark.django_db
def test_department_create_view_org_diff_tenant(client):
    tenant = tenants_factories.TenantFactory(name="my_tenant_name")
    organization = organizations_factories.OrganizationFactory()
    data = {"name": "department_name", "organization": str(organization.id)}
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)
    response = client.post(
        "/departments/",
        data=data,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=tenant.name,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_department_create_view(client):
    tenant = tenants_factories.TenantFactory(name="my_tenant_name")
    organization = organizations_factories.OrganizationFactory(tenant=tenant)
    data = {"name": "department_name", "organization": str(organization.id)}
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)
    response = client.post(
        "/departments/",
        data=data,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=tenant.name,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": ANY,
        "name": "department_name",
        "organization": str(organization.id),
    }
    assert models.Departament.objects.filter(tenant=tenant).count() == 1


@pytest.mark.django_db
def test_department_update_view(client):
    tenant = tenants_factories.TenantFactory(name="my_tenant_name")
    organization = organizations_factories.OrganizationFactory(tenant=tenant)
    department = factories.DepartmentFactory(
        name="org_name_old", tenant=tenant, organization=organization
    )
    data = {"name": "org_name_new", "organization": str(organization.id)}
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)
    response = client.put(
        f"/departments/{department.id}/",
        data=data,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=tenant.name,
    )
    assert response.status_code == status.HTTP_200_OK
    department.refresh_from_db()
    assert department.name == "org_name_new"
