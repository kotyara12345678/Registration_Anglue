FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

#  docker-compose up --build
#  http://127.0.0.1:8000/register/
#  docker exec -it pythonproject3-db-1 psql -U postgres
#  SELECT * FROM users;
#  http://localhost:15672