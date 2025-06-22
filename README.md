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
- [Running Tests](#running-tests)
d

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

## Running Tests

- **With Docker**:

  ```bash
	docker-compose run --rm web pytest -q
	
	
	
	docker-compose run --rm web \                         
  find . -type d -name "__pycache__" -exec rm -rf {} + && \
  find . -type f -name "*.pyc" -delete && \

(to delete cache)

  ```



---

