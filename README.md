# Bizixer War API

> برای نسخه فارسی، به [README.fa.md](README.fa.md) مراجعه کنید.

A modern FastAPI authentication backend for the Bizixer War project, using JWT tokens stored in secure HTTP-only cookies and SQLite as the default database.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)
![JWT](https://img.shields.io/badge/JWT-Authentication-000000?style=for-the-badge&logo=jsonwebtokens)

## Overview

This project provides a lightweight backend for user registration and login. It is designed for a small application that needs:

- user account creation
- secure login flow
- JWT-based session management
- role/front-based user metadata
- SQLite persistence with zero external database setup

The app is built with FastAPI and SQLModel, making it easy to extend with additional endpoints and business logic.

## Features

- User registration with unique usernames
- Login using username and password
- JWT generation with an expiration time of 30 days
- Secure cookie-based authentication using `httponly` cookies
- Support for multiple frontend identities via the `Front` enum
- Automatic table creation on startup
- Simple and readable project structure for rapid customization

## Supported Front Values

The `front` field accepts the following enum values:

- `mahdi`
- `fere`
- `gooji`

## Tech Stack

- Python 3.10+
- FastAPI
- SQLModel
- SQLite
- PyJWT
- python-dotenv

## Project Structure

```text
bizixer_war/
├── app.py
├── README.md
├── README.fa.md
├── .env
├── .gitignore
├── LICENSE
└── db.db
```

## Installation

1. Clone the repository

```bash
git clone https://github.com/your-username/bizixer_war.git
cd bizixer_war
```

2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install fastapi sqlmodel PyJWT python-dotenv uvicorn
```

4. Configure the environment secret

Create a `.env` file in the project root:

```env
sec=your_super_secret_key_here
```

> Never commit your real secret key to public repositories.

## Running the Server

```bash
uvicorn app:app --reload
```

By default, the app will create the SQLite database file automatically when it starts.

## API Endpoints

### 1) Register User

`POST /api/v1/register`

Request body:

```json
{
  "username": "john",
  "password": "secret123",
  "front": "mahdi"
}
```

Response:

```json
{
  "id": 1,
  "username": "john",
  "front": "mahdi"
}
```

### 2) Login User

`POST /api/v1/login`

Request body:

```json
{
  "username": "john",
  "password": "secret123",
  "front": "mahdi"
}
```

Response:

```json
{
  "id": 1,
  "username": "john",
  "front": "mahdi"
}
```

The backend also sets a JWT token in an HTTP-only cookie named `token`.

## Authentication Flow

- The user registers or logs in
- The backend creates a JWT containing the user ID, username, front value, and expiration timestamp
- The token is stored in a secure cookie
- Later requests can read the cookie and validate the session

## Example Usage with curl

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secret123","front":"mahdi"}' \
  -c cookies.txt
```

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secret123","front":"mahdi"}' \
  -c cookies.txt
```

## Notes

- This project is intentionally simple and easy to understand.
- It is ideal for prototypes, internal tools, or early-stage product APIs.
- You can extend the project with protected route decorators, more user fields, or a different database backend later.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Contributions, improvements, and feature ideas are welcome. If you want to improve the project, please open an issue or submit a pull request.
