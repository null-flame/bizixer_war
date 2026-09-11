# Bizixer War

<div align="center">

```
     ____   _   _   _  __  __   ___   _   _  _____  _____  _   _  
    / ___| | | | | | |/ / / /  / _ \ | \ | |/ ____|/ ____|| \ | |
   | |     | | | | | ' / / /  | | | ||  \| | |    | |     |  \| |
   | |___  | |_| | | . \ \ \  | |_| || |\  | |___ | |___ | |\  |
    \____|  \___/  |_|\_\\_\_\  \___/ |_| \_| \____| \____||_| \_|
                                                                 
```

**A Strategic Multi-Team Warfare Game API**

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL_3.0-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.html)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0+-008080.svg)](https://fastapi.tiangolo.com/)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Game Mechanics](#game-mechanics)
- [Project Structure](#project-structure)
- [License](#license)
- [Contributing](#contributing)

---

## Overview

**Bizixer War** is a strategic multiplayer warfare game built with FastAPI. Players join one of three factions (Mahdi, Fere, or Gooji) and compete to build factories, produce missiles, and attack enemy bases. The game features a resource-based economy where players must strategically manage their coin resources to expand their military capabilities.

---

## Features

### Core Features
- **Multi-Team System**: 3 distinct factions (Mahdi, Fere, Gooji)
- **Authentication**: Secure JWT-based authentication with cookie storage
- **Resource Management**: Coin-based economy with automatic generation
- **Factory System**: 4 tiers of factories (T1-T4) with increasing production rates
- **Missile System**: 4 tiers of missiles (T1-T4) with different damage and build times
- **Combat System**: Attack enemy players with strategic missile strikes
- **Queue System**: Asynchronous missile production with countdown timers
- **Leaderboard**: Real-time ranking of all players

### Game Entities

| Type | T1 | T2 | T3 | T4 |
|------|----|----|----|----|
| **Factory Cost** | 30 | 500 | 10,000 | 100,000 |
| **Factory Production (per hour)** | 12 | 125 | 625 | 2,083 |
| **Factory Health** | 90 | 1,500 | 15,000 | 150,000 |
| **Missile Cost** | 48 | 600 | 2,500 | 10,415 |
| **Missile Build Time (minutes)** | 5 | 30 | 120 | 240 |

---

## Technology Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for Python
- **Database**: [SQLModel](https://sqlmodel.tiangolo.com/) + [SQLAlchemy](https://www.sqlalchemy.org/) with [aiosqlite](https://github.com/jreese/aiosqlite) for async SQLite
- **Authentication**: JWT (JSON Web Tokens) with [python-jose](https://github.com/mpdavis/python-jose)
- **Validation**: [Pydantic](https://pydantic.dev/) for data validation
- **Environment**: [python-dotenv](https://github.com/theskumar/python-dotenv) for configuration
- **Type Hints**: Full Python type hints support

---

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/bizixer_war.git
   cd bizixer_war
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your secret key
   ```

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

6. **Access the API:**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Using pip (Alternative)

```bash
pip install flit
flit install
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# JWT Secret Key (REQUIRED)
sec=your-very-secure-secret-key-here

# Database URL (Optional - defaults to SQLite)
DATABASE_URL=sqlite+aiosqlite:///db.db
```

> **Important**: The `sec` variable is used for JWT token signing. Use a strong, random string (at least 32 characters).

---

## API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/register` | Register a new user |
| POST | `/api/v1/login` | Login and receive JWT token |

### Game Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/get_coin` | Collect generated coins |
| POST | `/api/v1/buy_factory` | Purchase factories |
| POST | `/api/v1/buy_missile` | Purchase missiles (enters production queue) |
| POST | `/api/v1/attack` | Attack another player |
| POST | `/api/v1/get_missiles` | Collect completed missiles from queue |
| GET | `/api/v1/info` | Get current user information |
| GET | `/api/v1/leaderboard` | Get all players ranking |

### Request Examples

**Register:**
```bash
curl -X POST "http://localhost:8000/api/v1/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "player1", "password": "secure123", "front": "mahdi"}'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/api/v1/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "player1", "password": "secure123"}'
```

**Buy Factory:**
```bash
curl -X POST "http://localhost:8000/api/v1/buy_factory" \
  -H "Content-Type: application/json" \
  -H "Cookie: token=YOUR_JWT_TOKEN" \
  -d '{"factory_type": "T1", "count": 1}'
```

**Attack:**
```bash
curl -X POST "http://localhost:8000/api/v1/attack" \
  -H "Content-Type: application/json" \
  -H "Cookie: token=YOUR_JWT_TOKEN" \
  -d '{"Tid": 2, "missile_type": "T1", "factory_type": "T1", "count": 1}'
```

---

## Game Mechanics

### Starting Resources
- **Initial Coins**: 500
- **Initial T1 Factories**: 100
- **Initial Missiles**: 0

### Coin Generation
Coins are generated automatically based on factory production rates. The longer you wait between collections, the more coins you accumulate. Each factory type produces coins at a different rate per hour.

**Production Formula:**
```
Total Coins = (F1 x 12/3600 + F2 x 125/3600 + F3 x 625/3600 + F4 x 2083/3600) x seconds_passed
```

### Factory Purchase
- Factories produce coins continuously
- Higher tier factories produce exponentially more
- Each factory costs coins to purchase
- No limit on factory count

### Missile System
- Missiles must be purchased with coins
- After purchase, missiles enter a production queue
- Each missile type has a different build time
- Missiles can be collected from the queue once ready
- Different missile types deal different damage

**Missile Damage Formula:**
```
Damage = Missile_Cost x Count
Factories Destroyed = Damage / Factory_Health
```

### Combat Rules
- Cannot attack players in the same faction
- Must have sufficient missiles for the attack
- Damage is calculated based on missile type and count
- Destroyed factories are subtracted from enemy count
- Minimum factory count is 0 (cannot go negative)

---

## Project Structure

```
bizixer_war/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py        # Main API router
│   │   ├── root.py          # Root endpoints
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py    # v1 API router
│   │       ├── auth.py      # Authentication endpoints
│   │       ├── coin.py      # Coin endpoints
│   │       ├── factory.py   # Factory endpoints
│   │       ├── missile.py   # Missile endpoints
│   │       └── info.py      # Info endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Game configuration & constants
│   │   ├── database.py      # Database setup & session management
│   │   └── security.py      # JWT authentication utilities
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   ├── queue.py         # Queue model
│   │   └── enums.py         # Enumerations (TType, Front)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication schemas
│   │   ├── missile.py       # Missile schemas
│   │   └── info.py          # Info schemas
│   └── services/
│       ├── __init__.py
│       ├── auth_service.py  # Authentication business logic
│       ├── coin_service.py  # Coin business logic
│       ├── factory_service.py # Factory business logic
│       ├── missile_service.py # Missile business logic
│       └── info.py          # Info business logic
├── .env                    # Environment variables
├── .gitignore
├── LICENSE                 # AGPL-3.0 License
├── pyproject.toml          # Project metadata
├── README.md               # This file
├── README.fa.md            # Persian documentation
└── requirements.txt        # Python dependencies
```

---

## License

This project is licensed under the **GNU Affero General Public License version 3 (AGPL-3.0)**.

[![AGPL-3.0 License](https://www.gnu.org/graphics/agplv3-with-text-155x51.png)](https://www.gnu.org/licenses/agpl-3.0.html)

### Key Points of AGPL-3.0:

- **Freedom to Use**: You are free to use, modify, and distribute the software
- **Copyleft**: Any modifications must also be licensed under AGPL-3.0
- **Source Availability**: If you run this software on a network server, you must make the source code available to users
- **Strong Copyleft**: The license extends to all derivative works
- **Patents**: Grants patent rights to users

> **Note**: This license ensures that all users have the freedom to access, modify, and share the software, even when used in network server applications.

For the full license text, see [LICENSE](LICENSE) file or visit [https://www.gnu.org/licenses/agpl-3.0.html](https://www.gnu.org/licenses/agpl-3.0.html)

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use type hints extensively
- Write docstrings for public functions
- Keep commits atomic and well-described

### Testing
- Test your changes thoroughly
- Ensure existing functionality is not broken
- Add tests for new features when applicable

---

## Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Check the [API Documentation](#api-documentation) for usage questions

---

<div align="center">

**Made with Python & FastAPI**  

*Strategy. Warfare. Victory.*

</div>

---

*Copyright (C) 2024 Bizixer War*  
*Licensed under GNU Affero General Public License v3.0*
