# recipe-box

![CI](https://github.com/helotrev4/recipe-box/actions/workflows/ci.yml/badge.svg)

A recipe management REST API built with FastAPI and PostgreSQL, containerized with Docker and deployed to Railway with an automated CI/CD pipeline.

## Tech Stack

### Frontend:

- React
- TypeScript
- CSS

### Backend:

- FastAPI
- Python

### Database

- PostgreSQL

### ORM (Database Access)

- SQLAlchemy

### Testing

- pytest

### Version Control

- GitHub
- Git

### CI/CD

- GitHub Actions

### Containerization

- Docker

### Cloud

- Railway

## Endpoints

| Method | Endpoint        | Description        |
| ------ | --------------- | ------------------ |
| GET    | `/`             | Get Root           |
| GET    | `/recipes`      | List all recipes   |
| GET    | `/recipes/{id}` | Get a recipe by ID |
| POST   | `/recipes`      | Create a recipe    |
| PUT    | `/recipes/{id}` | Update a recipe    |
| DELETE | `/recipes/{id}` | Delete a recipe    |

## Local Development without Docker

```bash
# If needed, this so PS can run local scripts like venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

```bash
# Run from root directory

backend\.venv\Scripts\activate

# Install dependancies

pip install -r requirements.txt

# Running the app (local dev server)

uvicorn backend.main:app --reload

http://127.0.0.1:8000
```

## Local Development with Docker

```bash

# Build image

docker build -t recipe-box .

# Run container (local container on machine)

docker run -p 8000:8000 -e DATABASE_URL="postgresql+asyncpg://postgres:PASSWORD@host.docker.internal:5433/recipebox" recipe-box

# Check app docs

http://localhost:8000/docs

```

## Testing:

```bash
pytest backend/tests/tests.py
```

## Railway:

recipe-box-production-cfbd.up.railway.app

<!-- ## Azure:

```bash
# installation
winget install Microsoft.AzureCLI

# login
az login

# Create a resource group to hold everything
az group create --name recipe-box-rg --location canadacentral

# Create Container registry to store Docker images
az acr create `
  --resource-group recipe-box-rg `
  --name recipeboxregistry `
  --sku Basic `
  --admin-enabled true
```

If command above doesn't work, try this:

```bash
az provider register --namespace Microsoft.ContainerRegistry

# Wait 30 seconds then check
az provider show --namespace Microsoft.ContainerRegistry --query registrationState

# If "Registered" and not "Registering"

az provider register --namespace Microsoft.DBforPostgreSQL

az provider show --namespace Microsoft.DBforPostgreSQL --query registrationState

az provider register --namespace Microsoft.Web

az provider show --namespace Microsoft.Web --query registrationState
```

```bash
# Create Postgres database server
az postgres flexible-server create `
  --resource-group recipe-box-rg `
  --location canadacentral `
  --name recipe-box-db `
  --admin-user recipebox_admin `
  --admin-password YourStrongPassword123! `
  --sku-name Standard_B1ms `
  --tier Burstable `
  --public-access 0.0.0.0

# Create Postgres database inside the server
az postgres flexible-server db create `
  --resource-group recipe-box-rg `
  --server-name recipe-box-db `
  --name recipebox

# Create the App Service plan, B1 is smallest paid tier (for Docker)
az appservice plan create `
  --name recipe-box-plan `
  --resource-group recipe-box-rg `
  --is-linux `
  --sku B1
``` -->

## Tech Stack

- **Backend** — FastAPI, Python 3.11
- **Database** — PostgreSQL (managed), SQLAlchemy async, Alembic
- **Testing** — pytest, pytest-asyncio, httpx
- **DevOps** — Docker, GitHub Actions CI/CD, Railway

## Live API

Base URL: `recipe-box-production-cfbd.up.railway.app`

API docs: `recipe-box-production-cfbd.up.railway.app/docs`

## CI/CD Pipeline

Every push to `main`:

1. GitHub Actions runs the test suite automatically
2. If tests pass, Railway deploys the latest Docker image
3. If tests fail, deployment is blocked
