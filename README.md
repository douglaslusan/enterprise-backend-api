# Enterprise Backend API

Modern backend API built with FastAPI, PostgreSQL, Docker and JWT Authentication.

## Stack

- Python
- FastAPI
- PostgreSQL
- Docker
- SQLAlchemy
- JWT Authentication
- Pydantic

## Features

- User registration
- Login authentication
- Password hashing with bcrypt
- JWT token generation
- PostgreSQL persistence
- Dockerized database

## Run Project

### Create virtual environment

```bash
python -m venv venv
```

### Activate virtual environment

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start PostgreSQL Docker

```bash
docker compose up -d 
```

### Run FastAPI

```bash
uvicorn app.main:app --reload
```

## Swagger

```text
http://127.0.0.1:8000/docs
```