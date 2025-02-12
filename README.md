# Multi-Tenant Django CRUD Application

## 📌 Project Overview
This project is a **Django-based prototype application** demonstrating a **multi-tenant architecture** with four organizational levels:
- **Tenant**
- **Organization**
- **Department**
- **Customer**

The goal of this project is to showcase a **scalable, secure, and well-structured Django application** with:
- **Data isolation** between tenants
- **Hierarchical access control**
- **REST API implementation** using Django REST Framework (DRF)
- **Containerized deployment** using Docker & Docker Compose

---

## 🚀 Tech Stack
- **Django** (Backend framework)
- **Django REST Framework (DRF)** (API development)
- **PostgreSQL** (Database)
- **Docker & Docker Compose** (Containerized deployment)
- **Postman Collection** (API testing)
- **Makefile** (Simplified command execution)

---

## 🔧 Setup & Installation



### Run the Application using Docker
Ensure you have **Docker** and **Docker Compose** installed, then run:
```sh
make run  # Builds and starts the application
```

This will:
- Build Docker images
- Start the Django application and database inside containers

### Migrate db
```sh
make migrate
```

### Access the Application
- API: [http://localhost:8000/api/](http://localhost:8000/api/)
- Django Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

### Run Shell & Tests
- Open Django shell:
  ```sh
  make shell
  ```
- Run tests:
  ```sh
  make test

### Setup postman
- Import postman collection: ```djangoCRUD.postman_collection.json```


---
