# Bizixer War API

> نسخه اصلی این پروژه به زبان انگلیسی در [README.md](README.md) قرار دارد.

این پروژه یک بک‌اند ساده و تمیز برای سیستم احراز هویت کاربران در پروژه Bizixer War است. این سرویس با FastAPI ساخته شده و از JWT برای مدیریت نشست کاربران استفاده می‌کند. توکن‌ها به‌صورت کوکی امن و HttpOnly ذخیره می‌شوند و به‌صورت پیش‌فرض از SQLite استفاده می‌کند.

## معرفی کوتاه

این API برای موارد زیر طراحی شده است:

- ثبت‌نام کاربر
- ورود کاربران
- مدیریت جلسات با JWT
- نگهداری داده‌ها در SQLite
- پشتیبانی از ارزش‌های مختلف برای فیلد `front`

## ویژگی‌ها

- ثبت‌نام با نام کاربری یکتا
- ورود با نام کاربری و رمز عبور
- تولید توکن JWT با تاریخ انقضا ۳۰ روز
- ذخیره توکن در کوکی امن
- پشتیبانی از مقادیر `mahdi`، `fere` و `gooji` برای فیلد `front`
- ساخت خودکار جدول‌ها هنگام اجرا

## تکنولوژی‌ها

- Python
- FastAPI
- SQLModel
- SQLite
- PyJWT
- python-dotenv

## نصب و اجرا

1. کلون کردن پروژه

```bash
git clone https://github.com/your-username/bizixer_war.git
cd bizixer_war
```

2. ایجاد و فعال‌سازی محیط مجازی

```bash
python -m venv .venv
source .venv/bin/activate
```

3. نصب وابستگی‌ها

```bash
pip install fastapi sqlmodel PyJWT python-dotenv uvicorn
```

4. تنظیم متغیر امنیتی

در ریشه پروژه یک فایل `.env` بسازید:

```env
sec=your_super_secret_key_here
```

> کلید واقعی را هرگز در مخزن عمومی commit نکنید.

5. راه‌اندازی سرور

```bash
uvicorn app:app --reload
```

## endpoint ها

### ثبت‌نام

`POST /api/v1/register`

بدنه درخواست:

```json
{
  "username": "john",
  "password": "secret123",
  "front": "mahdi"
}
```

### ورود

`POST /api/v1/login`

بدنه درخواست:

```json
{
  "username": "john",
  "password": "secret123",
  "front": "mahdi"
}
```

## نکات امنیتی

- توکن‌ها در کوکی `httponly` ذخیره می‌شوند.
- مقدار `sec` باید یک کلید امن و مخفی باشد.
- برای استفاده در محیط production، بهتر است علاوه بر SQLite، از دیتابیس مناسب‌تر و تنظیمات امنیتی قوی‌تر استفاده شود.

## لایسنس

این پروژه تحت مجوز MIT منتشر شده است. جزئیات کامل در [LICENSE](LICENSE) موجود است.

برای آشنایی با نسخه اصلی و جزئیات بیشتر، به [README.md](README.md) مراجعه کنید.
