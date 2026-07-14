# recipe-box

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

- Microsoft Azure
- Railway <- Azure doesn't allow

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

# Running the app

uvicorn backend.main:app --reload

http://127.0.0.1:8000
```

<!-- If not using Docs, these commands in terminal -->
<!--
curl.exe -X GET http://localhost:8000
curl.exe -X GET http://localhost:8000/rcipes/{num}

curl.exe -X POST http://localhost:8000/recipes?name=Spaghetti (old)
curl.exe -X POST http://localhost:8000/recipes -H "Content-Type: application/json" -d '{\"name\": \"Spaghetti\"}'
curl.exe -X POST http://localhost:8000/recipes -H "Content-Type: application/json" -d '{\"name\": \"Spaghetti\", \"calories\": 300}' -->

## Local Development with Docker

```bash

# Build image

docker build -t recipe-box .

# Run container

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

## Azure:

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
```
