from unittest.mock import ANY

import pytest
from customers import models
from customers.tests import factories
from departments.tests import factories as departments_factories
from organizations.tests import factories as organizations_factories
from rest_framework import status
from rest_framework.authtoken.models import Token
from tenants.tests import factories as tenants_factories
from utils.tests import factories as utils_factories


@pytest.fixture()
def test_data():
    tenant = tenants_factories.TenantFactory(name="my_tenant_name")
    organization = organizations_factories.OrganizationFactory(tenant=tenant)
    department = departments_factories.DepartmentFactory(organization=organization)
    customer1 = factories.CustomerFactory(tenant=tenant, department=department)
    customer2 = factories.CustomerFactory(tenant=tenant, department=department)
    customer3 = factories.CustomerFactory(
        tenant=tenant
    )  # customer4 has different department
    factories.CustomerFactory()  # customer4 has different tenant
    return {
        "tenant": tenant,
        "organization": organization,
        "department": department,
        "customers": [customer1, customer2, customer3],
    }


@pytest.mark.django_db
def test_customer_view_unauthorized(client):
    customer = factories.CustomerFactory()
    response = client.get(
        f"/customers/{customer.id}/",
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_customer_view_no_tenant(client):
    customer = factories.CustomerFactory()
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.get(
        f"/customers/{customer.id}/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_customer_retreive_view(client, test_data):
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.get(
        f'/customers/{test_data["customers"][0].id}/',
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=test_data["tenant"].name,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": str(test_data["customers"][0].id),
        "name": test_data["customers"][0].name,
        "department": str(test_data["customers"][0].department.id),
    }


@pytest.mark.django_db
def test_customer_list_view(client, test_data):
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)
    customer1 = test_data["customers"][0]
    customer2 = test_data["customers"][1]
    customer3 = test_data["customers"][2]
    response = client.get(
        "/customers/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=test_data["tenant"].name,
    )
    assert response.status_code == status.HTTP_200_OK
    resp = response.json()
    assert len(resp) == 3
    assert resp == [
        {
            "id": str(customer1.id),
            "name": customer1.name,
            "department": str(customer1.department.id),
        },
        {
            "id": str(customer2.id),
            "name": customer2.name,
            "department": str(customer2.department.id),
        },
        {
            "id": str(customer3.id),
            "name": customer3.name,
            "department": str(customer3.department.id),
        },
    ]


@pytest.mark.django_db
def test_customer_list_view_organization_filter(client, test_data):
    customer1 = test_data["customers"][0]
    customer2 = test_data["customers"][1]
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.get(
        f'/customers/?department={test_data["department"].id}',
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=test_data["tenant"].name,
    )
    assert response.status_code == status.HTTP_200_OK
    resp = response.json()
    assert len(resp) == 2
    assert resp == [
        {
            "id": str(customer1.id),
            "name": customer1.name,
            "department": str(customer1.department.id),
        },
        {
            "id": str(customer2.id),
            "name": customer2.name,
            "department": str(customer2.department.id),
        },
    ]


@pytest.mark.django_db
def test_customer_delete_view_no_tenant(client):
    customer1 = factories.CustomerFactory()
    assert models.Departament.objects.count() == 1
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.delete(
        f"/customers/{customer1.id}/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_customer_delete_view(client, test_data):
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)
    customer1 = test_data["customers"][0]
    assert models.Customer.objects.count() == 4

    response = client.delete(
        f"/customers/{customer1.id}/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=test_data["tenant"].name,
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert models.Customer.objects.count() == 3


#
@pytest.mark.django_db
def test_customer_delete_view_different_tenant(client):
    tenant = tenants_factories.TenantFactory(name="diff_tenant")
    customer1 = factories.CustomerFactory()
    assert models.Customer.objects.count() == 1
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)

    response = client.delete(
        f"/customers/{customer1.id}/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=tenant.name,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert models.Customer.objects.count() == 1


@pytest.mark.django_db
def test_customer_create_view_org_diff_tenant(client):
    tenant = tenants_factories.TenantFactory(name="my_tenant_name")
    department = departments_factories.DepartmentFactory()
    data = {"name": "customer_name", "department": str(department.id)}
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)
    response = client.post(
        "/customers/",
        data=data,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=tenant.name,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_customer_create_view(client):
    tenant = tenants_factories.TenantFactory(name="my_tenant_name")
    department = departments_factories.DepartmentFactory(tenant=tenant)
    data = {"name": "customer_name", "department": str(department.id)}
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)
    response = client.post(
        "/customers/",
        data=data,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=tenant.name,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": ANY,
        "name": "customer_name",
        "department": str(department.id),
    }
    assert models.Customer.objects.filter(tenant=tenant).count() == 1


@pytest.mark.django_db
def test_customer_update_view(client):
    tenant = tenants_factories.TenantFactory(name="my_tenant_name")
    organization = organizations_factories.OrganizationFactory(tenant=tenant)
    department = departments_factories.DepartmentFactory(
        tenant=tenant, organization=organization
    )
    customer = factories.CustomerFactory(
        name="customer_name_old", tenant=tenant, department=department
    )
    data = {"name": "customer_name_new", "department": str(department.id)}
    user = utils_factories.UserFactory()
    token = Token.objects.create(user=user)
    response = client.put(
        f"/customers/{customer.id}/",
        data=data,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {token.key}",
        HTTP_X_TENANT=tenant.name,
    )
    assert response.status_code == status.HTTP_200_OK
    customer.refresh_from_db()
    assert customer.name == "customer_name_new"
