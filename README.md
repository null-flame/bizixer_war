# Bizixer War

## بازی استراتژیک جنگ کارخانه‌ها

یک بازی استراتژیک چند نفره آنلاین که در آن بازیکنان با خرید کارخانه‌ها و موشک‌ها، به یکدیگر حمله می‌کنند.

## ویژگی‌ها

- **سیستم ثبت‌نام و ورود** با احراز هویت JWT
- **مدیریت کارخانه‌ها** (T1, T2, T3, T4) با تولید خودکار سکه
- **سیستم خرید موشک** با زمان ساخت متفاوت برای هر نوع
- **سیستم حمله** به کارخانه‌های حریف
- **سیستم نوبت‌بندی** برای ساخت موشک‌ها
- **پشتیبانی از ۳ جبهه** (mahdi, fere, gooji)
- **دیتابیس SQLite** با پشتیبانی Async

## فناوری‌ها

- **Backend**: FastAPI
- **Database**: SQLite (Async) + SQLModel + SQLAlchemy
- **Authentication**: JWT (python-jose)
- **Async**: anyio + aiosqlite
- **Validation**: Pydantic v2

## نصب و اجرا

### پیش‌نیازها

- Python 3.10+
- pip

### نصب وابستگی‌ها

```bash
git clone https://github.com/null-flame/bizixer_war.git
cd bizixer_war
pip install -r requirements.txt
```

### تنظیمات محیطی

```bash
# ایجاد فایل .env
cp .env.example .env

# ویرایش فایل .env
nano .env
```

محتویات فایل `.env`:

```env
# کلید مخفی برای JWT
sec=your_super_secret_jwt_key_here

# تنظیمات دیتابیس (اختیاری - پیش‌فرض: sqlite+aiosqlite:///db.db)
# DB_URL=sqlite+aiosqlite:///db.db
```

### اجرا

```bash
# اجرا در حالت توسعه
uvicorn app.main:app --reload --port 8000

# اجرا در حالت تولید
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## ساختار پروژه

```
bizixer_war/
├── app/
│   ├── __init__.py
│   ├── main.py              # نقطه ورود برنامه
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependency Injections
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py    # مسیریاب اصلی
│   │       ├── auth.py      # APIهای احراز هویت
│   │       ├── coin.py      # APIهای سکه
│   │       ├── factory.py   # APIهای کارخانه
│   │       ├── missile.py   # APIهای موشک
│   │       └── info.py      # APIهای اطلاعات
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # تنظیمات برنامه
│   │   ├── database.py      # اتصال به دیتابیس
│   │   └── security.py      # امنیت و JWT
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # مدل کاربر
│   │   ├── queue.py         # مدل صف ساخت
│   │   └── enums.py         # Enumerations
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py          # Schemaهای احراز هویت
│   │   ├── info.py          # Schemaهای اطلاعات
│   │   └── missile.py       # Schemaهای موشک
│   │
│   └── services/
│       ├── __init__.py
│       ├── auth_service.py  # سرویس احراز هویت
│       ├── coin_service.py  # سرویس سکه
│       ├── factory_service.py # سرویس کارخانه
│       ├── missile_service.py # سرویس موشک
│       └── info.py          # سرویس اطلاعات
│
├── requirements.txt         # وابستگی‌ها
├── .env.example            # نمونه فایل محیطی
└── README.md               # مستندات
```

## API Documentation

پس از اجرا، مستندات API به صورت خودکار در آدرس زیر قابل دسترسی است:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### احراز هویت

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/register` | ثبت‌نام کاربر جدید |
| POST | `/api/v1/login` | ورود کاربر |

### سکه

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/get_coin` | دریافت سکه‌های تولید شده |

### کارخانه

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/buy_factory` | خرید کارخانه |

### موشک

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/buy_missile` | خرید موشک |
| POST | `/api/v1/attack` | حمله به حریف |
| POST | `/api/v1/get_missiles` | دریافت موشک‌های ساخته شده |

### اطلاعات

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/info` | دریافت اطلاعات کاربر |
| GET | `/api/v1/leaderboard` | دریافت لیست کاربران |

## مدل‌های داده

### انواع کارخانه و موشک

| Type | Cost (Coin) | Production (Coin/Hour) | Health |
|------|-------------|------------------------|--------|
| T1 | 30 | 12/hr | 90 |
| T2 | 500 | 125/hr | 1500 |
| T3 | 10,000 | 625/hr | 15,000 |
| T4 | 100,000 | 2,083/hr | 150,000 |

### هزینه موشک‌ها

| Type | Cost (Coin) | Build Time (Minutes) |
|------|-------------|---------------------|
| T1 | 48 | 5 |
| T2 | 600 | 30 |
| T3 | 2,500 | 120 |
| T4 | 10,415 | 240 |

### جبهه‌ها

- `mahdi`
- `fere`
- `gooji`

## قوانین بازی

1. هر کاربر با 500 سکه و 100 کارخانه T1 شروع می‌کند
2. کارخانه‌ها به صورت خودکار سکه تولید می‌کنند
3. موشک‌ها قبل از استفاده باید ساخته شوند
4. نمی‌توان به کاربران هم‌جبهه حمله کرد
5. هر حمله به کارخانه‌های حریف آسیب می‌زند

## توسعه

### تست‌ها

```bash
# اجرا کردن تست‌ها
pytest

# اجرا با پوشش کد
pytest --cov=app
```

### Type Checking

```bash
mypy app/
```

### Formatting

```bash
# مرتب‌سازی کد
ruff check .
ruff format .

# یا با black
black app/
isort app/
```

## مشارکت

1. Fork کردن repository
2. ایجاد branch جدید (`git checkout -b feature/your-feature`)
3. Commit کردن تغییرات (`git commit -m 'Add some feature'`)
4. Push کردن به branch (`git push origin feature/your-feature`)
5. ایجاد Pull Request

## مجوز

MIT License

---

Developed by [null-flame](https://github.com/null-flame)
