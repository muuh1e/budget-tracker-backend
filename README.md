# PhotoCart Backend

A Django-based REST API backend for the PhotoCart application, handling user authentication, financial transactions, and photo order processing with background tasks.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Technologies](#technologies)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Docker Setup & Usage](#docker-setup--usage)
-  [Exploring the API routes](#exploring-the-api-routes)
- [Running Tests](#running-tests)


---

## Project Overview

PhotoCart Backend provides:

- User management & permissions
- Financial transaction tracking
- Celery-based background tasks (sending emails, scheduled jobs)
- RESTful API endpoints via Django REST Framework

---

## Technologies

- Python 3.12
- Django 4.x
- Django REST Framework
- Celery, celery-beat & Redis
- PostgreSQL
- Docker & Docker Compose
- Swagger
- Django-filters
---

## Prerequisites

- **Git** to clone the repository
- **Docker Engine** (>= 20.x) and **Docker Compose** (>= 1.29.x) for containerized setup
- (Optional) **Python 3.12** and **virtualenv** for local development

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/muuh1e/budget-tracker-backend.git
   cd budget-tracker-backend
   ```

2. \*\*Create \*\*\`\` (if not already present)

   ```bash
   cp .env.example .env
   ```

3. **Populate** `.env` with your own secrets

---

## Configuration

- Copy `.env.example` → `.env` and fill in values.
- Ensure `.env` is listed in `.gitignore` to avoid committing real secrets.
- For Docker builds, you can either export your HOST\_UID and HOST\_GID in your shell or add them to `.env`:
  ```bash
  export HOST_UID=$(id -u)
  export HOST_GID=$(id -g)
  ```

---

## Docker Setup & Usage

1. **Build & start containers**

   ```bash
   docker-compose build --no-cache
   docker-compose up
   ```

2. The following services will start:

   - **web**: Django API ([http://localhost:8000](http://localhost:8000))
   - **db**: PostgreSQL (port 5432)
   - **redis**: Redis for Celery
   - **smtp4dev**: Local SMTP server (UI: [http://localhost:5000](http://localhost:5000), SMTP: 2525)
   - **celery**: Celery worker
   - **celery-beat**: Celery scheduler

3. **Common commands**

   - View logs: `docker-compose logs -f web`

   - Run a shell in the web container: `docker-compose exec web bash`

   - Stop & remove containers: `docker-compose down`

   - Rebuild without cache: `docker-compose build --no-cache`

   - View logs: `docker-compose logs -f web`

   - Run a shell in the web container: `docker-compose exec web bash`

   - Stop & remove containers: `docker-compose down`

   - Rebuild without cache: `docker-compose build --no-cache`

---

---

## Exploring the API Routes

Once your backend is up (e.g. at `http://localhost:8000`), you can discover and exercise every endpoint in three ways:

### 1. Swagger UI  
Visit  
```
http://localhost:8000/swagger/
```
An interactive, “try-it-out” interface showing all paths, methods, parameters, request/response schemas and examples.

### 2. ReDoc  
Visit  
```
http://localhost:8000/redoc/
```
A clean, read-only documentation layout with the same comprehensive schema details.

### 3. DRF’s Browsable API  
Point your browser at  
```
http://localhost:8000/api/
```
Drill into each resource (e.g. `categories/`, `transactions/`, `dashboard/`), see available HTTP methods, and exercise them directly from the browser.

---

### Common Endpoints

#### Authentication (`/api/auth/`)  
- **POST** `register/` → Create a new user  
- **POST** `token/` → Obtain JWT access & refresh tokens  
- **POST** `token/refresh/` → Refresh your access token  
- **POST** `logout/` → Invalidate your tokens

#### Categories (`/api/categories/`)  
- **GET** `/` → List your categories  
- **POST** `/` → Create a category  
- **GET** `/{id}/` → Retrieve a category  
- **PUT** `/{id}/` or **PATCH** `/{id}/` → Update a category  
- **DELETE** `/{id}/` → Delete a category  

#### Transactions (`/api/transactions/`)  
- **GET** `/` → List transactions  
  - Query params:  
    - `date=YYYY-MM-DD`  
    - `type=INCOME|EXPENSE`  
    - `category_id=<id>`  
- **POST** `/` → Create a transaction  
- **GET** `/{id}/` → Retrieve a transaction  
- **PUT** `/{id}/` or **PATCH** `/{id}/` → Update a transaction  
- **DELETE** `/{id}/` → Delete a transaction  
- **GET** `/by-category/` → Aggregate totals & counts per category

#### Dashboard (`/api/dashboard/`)  
- **GET** `/` → Get a summary of total income, total expenses, and current balance


## Running Tests

- **With Docker**:

  ```bash
	docker-compose run --rm web pytest -q
	
	
	
	docker-compose run --rm web \                         
  find . -type d -name "__pycache__" -exec rm -rf {} + && \
  find . -type f -name "*.pyc" -delete && \

(to delete cache)
