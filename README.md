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

## Side Notes and Commands

pip install -r requirements.txt

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

<!-- From the root directory -->

backend\.venv\Scripts\activate

venv\Scripts\activate

<!-- Running the app -->

uvicorn backend.main:app --reload

http://127.0.0.1:8000
http://localhost:8000/docs

curl.exe -X GET http://localhost:8000
curl.exe -X GET http://localhost:8000/recipes/{num}

curl.exe -X POST http://localhost:8000/recipes?name=Spaghetti (old)
curl.exe -X POST http://localhost:8000/recipes -H "Content-Type: application/json" -d '{\"name\": \"Spaghetti\"}'
curl.exe -X POST http://localhost:8000/recipes -H "Content-Type: application/json" -d '{\"name\": \"Spaghetti\", \"calories\": 300}'

## Testing:

pytest backend/tests/tests.py

## Docker:

docker build -t recipe-box .

docker run -p 8000:8000 -e DATABASE_URL="postgresql+asyncpg://postgres:PASSWORD@host.docker.internal:5433/recipebox" recipe-box
