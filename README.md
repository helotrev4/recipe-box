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

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate

pip install fastapi uvicorn sqlalchemy psycopg2-binary

uvicorn main:app --reload

http://127.0.0.1:8000
http://localhost:8000/docs

curl.exe -X GET http://localhost:8000
curl.exe -X GET http://localhost:8000/recipes/{num}

curl.exe -X POST http://localhost:8000/recipes?name=Spaghetti (old)
curl.exe -X POST http://localhost:8000/recipes -H "Content-Type: application/json" -d '{\"name\": \"Spaghetti\"}'
curl.exe -X POST http://localhost:8000/recipes -H "Content-Type: application/json" -d '{\"name\": \"Spaghetti\", \"calories\": 300}'
