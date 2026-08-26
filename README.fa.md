# Bizixer War API

<div align="center">
  <img src="https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=1400&q=80" alt="بنر پروژه Bizixer War" width="100%" />
</div>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite" alt="SQLite" />
  <img src="https://img.shields.io/badge/JWT-Authentication-000000?style=for-the-badge&logo=jsonwebtokens" alt="JWT" />
  <img src="https://img.shields.io/badge/License-AGPLv3-red?style=for-the-badge" alt="AGPLv3" />
</p>

> بک‌اند احراز هویت آماده برای پروژه بازی Bizixer War.

Bizixer War یک بک‌اند سبک و مدرن است که برای یک برنامه وب یا بازی مبتنی بر مرورگر طراحی شده تا کاربران بتوانند هویت خود را به‌صورت امن مدیریت کنند، ورود سریع داشته باشند و نشست‌های دائمی و مطمئن را تجربه کنند. این پروژه با هدف ساده‌بودن، تمیز بودن و توسعه‌پذیری بالا ساخته شده است تا در آینده به یک بک‌اند کامل بازی تبدیل شود با قابلیت‌های مثل همخوانی، پروفایل کاربر، انبار، افتخارات و پیشرفت حساب.

## معرفی پروژه

این API پایه و اساس هویت کاربران در یک پروژه بازی را فراهم می‌کند:

- ثبت‌نام بازیکن
- ورود امن
- احراز هویت مبتنی بر JWT
- ذخیره نشست در کوکی
- پیگیری هویت `front` یا شخصیت بازیکن
- ذخیره داده‌ها با SQLite
- معماری ساده و آماده برای گسترش

این سرویس با FastAPI و SQLModel ساخته شده و همین موضوع باعث می‌شود کدها خوانا، قابل توسعه و سریع برای افزودن قابلیت‌های جدید باقی بمانند.

<div align="center">
  <img src="https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=1200&q=80" alt="محیط بازی" width="48%" />
  <img src="https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=1200&q=80" alt="رابط کاربری بازی" width="48%" />
</div>

## ایده بازی

پروژه به سمت یک تجربه بازی رقابتی یا استراتژیک طراحی شده است؛ جایی که هر بازیکن یک هویت یا نام‌عامل مخصوص به خود دارد و می‌تواند یکی از گزینه‌های زیر را انتخاب کند:

- `mahdi`
- `fere`
- `gooji`

این گزینه‌ها به پروژه اجازه می‌دهند تا چندین «front» یا نسخه‌ی متفاوت تجربه‌ی کاربری را با یک سیستم احراز هویت واحد پشتیبانی کند.

## ویژگی‌ها

- ثبت‌نام با نام‌کاربری یکتا
- ورود امن با نام‌کاربری و رمز عبور
- تولید JWT با اعتبار ۳۰ روزه
- احراز هویت از طریق کوکی با تنظیم `httponly`
- ساخت خودکار دیتابیس در زمان اجرا
- پشتیبانی از enumهای مختلف برای فیلد `front`
- طراحی ساده و مناسب برای پروژه‌های گیمینگ
- راه‌اندازی سریع بدون نیاز به دیتابیس خارجی

## تکنولوژی‌های مورد استفاده

- Python 3.10+
- FastAPI
- SQLModel
- SQLite
- PyJWT
- python-dotenv
- Uvicorn

## مقادیر مجاز Front

فیلد `front` فقط مجاز به یکی از مقادیر زیر است:

- `mahdi`
- `fere`
- `gooji`

این مقادیر برای تفاوت‌بخشی میان تجربه‌ها یا هویت‌های مختلف بازیکن استفاده می‌شوند.

## ساختار پروژه

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

## نصب و راه‌اندازی

### 1) کلون کردن پروژه

```bash
git clone https://github.com/your-username/bizixer_war.git
cd bizixer_war
```

### 2) ایجاد و فعال‌سازی محیط مجازی

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3) نصب وابستگی‌ها

```bash
pip install fastapi sqlmodel PyJWT python-dotenv uvicorn
```

### 4) تنظیم متغیرهای محیطی

یک فایل `.env` در ریشه پروژه بسازید:

```env
sec=your_super_secret_key_here
```

> این کلید را هرگز در مخزن عمومی منتشر نکنید و برای محیط تولید کاملاً محرمانه نگه‌ دارید.

## اجرای سرور

```bash
uvicorn app:app --reload
```

پس از اجرا، برنامه به‌صورت خودکار دیتابیس SQLite را می‌سازد و در صورت نبودن جدول‌ها، آن‌ها را ایجاد می‌کند.

## Endpoint ها

### ثبت‌نام بازیکن

`POST /api/v1/register`

بدنه درخواست:

```json
{
  "username": "john",
  "password": "secret123",
  "front": "mahdi"
}
```

پاسخ موفق:

```json
{
  "id": 1,
  "username": "john",
  "front": "mahdi"
}
```

### ورود بازیکن

`POST /api/v1/login`

بدنه درخواست:

```json
{
  "username": "john",
  "password": "secret123",
  "front": "mahdi"
}
```

پاسخ موفق:

```json
{
  "id": 1,
  "username": "john",
  "front": "mahdi"
}
```

در کنار این پاسخ، سرور یک کوکی HTTP-only با نام `token` برای مدیریت نشست کاربر تنظیم می‌کند.

## جریان احراز هویت

1. بازیکن ثبت‌نام یا ورود انجام می‌دهد.
2. بک‌اند اعتبار اطلاعات را بررسی می‌کند.
3. یک JWT با شامل شناسه کاربر، نام‌کاربری، مقدار `front` و زمان انقضا ساخته می‌شود.
4. توکن در کوکی امن و `httponly` ذخیره می‌شود.
5. درخواست‌های بعدی با خواندن این کوکی، نشست کاربر را تأیید می‌کنند.

## مثال استفاده با curl

### ثبت‌نام

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/register"   -H "Content-Type: application/json"   -d '{"username":"john","password":"secret123","front":"mahdi"}'   -c cookies.txt
```

### ورود

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/login"   -H "Content-Type: application/json"   -d '{"username":"john","password":"secret123","front":"mahdi"}'   -c cookies.txt
```

## نکات امنیتی

- توکن‌ها در کوکی‌های امن و HTTP-only ذخیره می‌شوند.
- مقدار `sec` باید یک کلید قوی و محرمانه باشد.
- تنظیمات حساس را با متغیرهای محیطی مدیریت کنید، نه کد‌گذاری مستقیم.
- برای محیط production، بهتر است دیتابیس قوی‌تر و سیاست‌های امنیتی بیشتری اعمال شود.


## گالری

<div align="center">
  <img src="https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?auto=format&fit=crop&w=1200&q=80" alt="پروفایل بازیکن" width="32%" />
  <img src="https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?auto=format&fit=crop&w=1200&q=80" alt="محیط نبرد" width="32%" />
  <img src="https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?auto=format&fit=crop&w=1200&q=80" alt="صحنه بازی" width="32%" />
</div>

## نقشه راه

این پروژه یک پایه‌ی خوب برای یک سیستم بازی است و در آینده می‌تواند توسعه پیدا کند تا شامل این امکانات شود:

- API برای پروفایل بازیکن
- جدول امتیاز و رتبه‌بندی
- سرویس هم‌تاختی و match-making
- منطق نبرد یا ماموریت‌ها
- انبار و ذخیره‌سازی آیتم‌ها
- پنل ادمین و مدیریت کاربران
- سخت‌سازی CORS و تنظیمات deployment

## مجوز

این پروژه تحت مجوز GNU Affero General Public License v3.0 (AGPL-3.0) منتشر شده است.

متن کامل مجوز در فایل [LICENSE](LICENSE) موجود است.

## مشارکت

مشارکت و پیشنهادهای بهبود خوش‌آمدگویی هستند. اگر می‌خواهید ویژگی جدیدی اضافه کنید، پروژه را بهتر کنید یا بخش‌های گیمینگ را توسعه دهید، می‌توانید یک issue باز کنید یا pull request ارسال کنید.

## جمع‌بندی نهایی

Bizixer War با تمرکز بر سرعت، ساختار تمیز و توسعه‌پذیری بالا ساخته شده است. این پروژه نقطه شروعی عالی برای تبدیل یک ایده‌ی ساده‌ی بازی به یک بک‌اند کامل با احراز هویت، مدیریت کاربران و سیستم‌های آینده‌ی گیمینگ است.
