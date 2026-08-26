# Bizixer War API

<div align="center">
  <img src="https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=1400&q=80" alt="Bizixer War banner" width="100%" />
</div>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite" alt="SQLite" />
  <img src="https://img.shields.io/badge/JWT-Authentication-000000?style=for-the-badge&logo=jsonwebtokens" alt="JWT" />
  <img src="https://img.shields.io/badge/License-AGPLv3-red?style=for-the-badge" alt="AGPLv3" />
</p>

> A game-ready authentication backend for the Bizixer War ecosystem.

Bizixer War is a lightweight, modern backend designed for a browser-based or game-inspired web app where players need secure identity management, fast login flows, and persistent user sessions. This project is intentionally minimal, clean, and easy to extend for real gameplay features such as matchmaking, profiles, inventory, achievements, and account progression.

## Overview

This API provides the foundation for user identity in a game project:

- player registration
- secure login
- JWT-based authentication
- cookie-based session storage
- role/front identity tracking
- SQLite-powered persistence
- simple architecture for future expansion

It is built with FastAPI and SQLModel, which makes it easy to evolve into a more complete game backend while keeping the codebase readable and developer-friendly.

<div align="center">
  <img src="https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=1200&q=80" alt="Game environment" width="48%" />
  <img src="https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=1200&q=80" alt="Game UI" width="48%" />
</div>

## Game Concept

The project is oriented around a competitive or strategy-inspired gaming experience where each player can choose a unique identity and front profile, such as:

- `mahdi`
- `fere`
- `gooji`

This allows the backend to support multiple front identities or player origins while keeping a single authentication system behind the scenes.

## Features

- unique username registration
- secure username + password login
- JWT generation with a 30-day expiration window
- HTTP-only cookie authentication
- automatic database creation on startup
- flexible `front` enum support
- simple API design suited for game projects
- fast setup with no external DB required

## Tech Stack

- Python 3.10+
- FastAPI
- SQLModel
- SQLite
- PyJWT
- python-dotenv
- Uvicorn

## Supported Front Values

The `front` field is validated against the following values:

- `mahdi`
- `fere`
- `gooji`

These values help differentiate player-facing experiences or UI variants across the project.

## Project Structure

```text
bizixer_war/
├── app.py
├── README.md
├── README.fa.md
├── .env
├── .gitignore
├── LICENSE
├── db.db
└── .venv/
```

## Installation

### 1) Clone the project

```bash
git clone https://github.com/your-username/bizixer_war.git
cd bizixer_war
```

### 2) Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install fastapi sqlmodel PyJWT python-dotenv uvicorn
```

### 4) Create environment variables

Create a `.env` file in the project root:

```env
sec=your_super_secret_key_here
```

> Keep this secret truly private. Never commit real production secrets to version control.

## Run the Server

```bash
uvicorn app:app --reload
```

Once started, the app will automatically initialize the SQLite database and create the required tables if they do not already exist.

## API Endpoints

### Register Player

`POST /api/v1/register`

Request body:

```json
{
  "username": "john",
  "password": "secret123",
  "front": "mahdi"
}
```

Successful response:

```json
{
  "id": 1,
  "username": "john",
  "front": "mahdi"
}
```

### Login Player

`POST /api/v1/login`

Request body:

```json
{
  "username": "john",
  "password": "secret123",
  "front": "mahdi"
}
```

Successful response:

```json
{
  "id": 1,
  "username": "john",
  "front": "mahdi"
}
```

The service also sets an HTTP-only cookie named `token` for authenticated sessions.

## Authentication Flow

1. A player registers or logs in.
2. The backend verifies the credentials.
3. A JWT is created with the user ID, username, front value, and expiration timestamp.
4. The token is stored in a secure `httponly` cookie.
5. Later requests can validate the session using that cookie.

## Example Usage with curl

### Register

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/register"   -H "Content-Type: application/json"   -d '{"username":"john","password":"secret123","front":"mahdi"}'   -c cookies.txt
```

### Login

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/login"   -H "Content-Type: application/json"   -d '{"username":"john","password":"secret123","front":"mahdi"}'   -c cookies.txt
```

## Security Notes

- JWTs are stored in secure, HTTP-only cookies.
- The `sec` value should be a strong secret key.
- Use environment variables for configuration instead of hardcoding secrets.
- For production deployment, consider stronger database choices and security policies.


## Game Gallery

<div align="center">
  <img src="https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?auto=format&fit=crop&w=1200&q=80" alt="Player profile" width="32%" />
  <img src="https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?auto=format&fit=crop&w=1200&q=80" alt="Arena" width="32%" />
  <img src="https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?auto=format&fit=crop&w=1200&q=80" alt="Battle scene" width="32%" />
</div>

## Roadmap

This project is a solid backend foundation for a game system. Future improvements may include:

- player profile endpoints
- leaderboard and ranking APIs
- matchmaking service
- battle or mission logic
- inventory and inventory persistence
- admin panel and moderation tools
- CORS and deployment hardening

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).

See the [LICENSE](LICENSE) file for the full legal text.

## Contributing

Contributions are welcome. If you want to improve the project, add features, or refine the game backend, feel free to open an issue or submit a pull request.

## Final Note

Bizixer War is built for fast iteration, clear structure, and easy expansion. It provides a strong starting point for turning a simple game idea into a full-featured backend with authentication, identity management, and future gameplay systems.
