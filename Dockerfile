FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# uses $PORT is it exists, only falls back to 8000 if $PORT isn't set
CMD ["sh", "-c", "python -m uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

# inside the [] means exec form, runs sh directly with explicit arguments