version: '3'
services:
  backend:
    container_name: backend
    restart: unless-stopped
    build: .
    ports:
      - 80:8000
    working_dir: /root/fastapi
    tty: true
    environment:
      - DB_HOST=pgsql
      - DB_PORT=5432
      - DB_DATABASE=postgres
      - DB_USER=postgres
      - DB_PASSWORD=postgres
    volumes:
      - ./fastapi:/root/fastapi
    depends_on:
      - pgsql
    command:
      - "/bin/sh"
      - "-c"
      - "sh ./wait-for-postgres.sh && uvicorn api.main:app --reload --host 0.0.0.0 --port 8000"

  pgsql:
    image: postgres:13.4
    container_name: pgsql
    ports:
      - 5432:5432
    volumes:
      - ./pgsql/init:/docker-entrypoint-initdb.d
      - ./pgsql/data:/var/lib/postgresql/data
    restart: unless-stopped
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_DB=postgres
