# 🚗 DrivePay


## ✨ Основные возможности

* 🚗 Автомобили и товары
* 📄 Отдельная страница каждого автомобиля
* 💳 Оплата через **Stripe Checkout**
* 🔐 Безопасная работа с Stripe Secret Key через environment variables
* 📦 Автоматическое создание Order при покупке
* 🆔 Уникальный Order ID для каждого заказа
* ⏳ Order status: `pending`
* ✅ После успешной оплаты: `paid`
* 🔎 Поиск заказа по Order ID
* 📋 Копирование Order ID
* 🎉 Отдельная страница успешной оплаты
* ❌ Отдельная страница отменённой оплаты
* 🗄️ Хранение заказов и автомобилей в базе данных
* ⚙️ Django Admin для управления автомобилями и заказами

---

## 💳 Как работает оплата

Процесс оплаты построен следующим образом:

```text
Пользователь
     ↓
Выбирает автомобиль
     ↓
Buy Now
     ↓
Создаётся Order со статусом PENDING
     ↓
Создаётся Stripe Checkout Session
     ↓
Пользователь переходит на Stripe
     ↓
Производится оплата
     ↓
Stripe возвращает пользователя на Success URL
     ↓
Django получает session_id
     ↓
Проверяет payment_status через Stripe API
     ↓
payment_status == "paid"
     ↓
Order → PAID
     ↓
Order сохраняется в Database
```

Таким образом, успешный переход пользователя на страницу Success сам по себе не считается подтверждением оплаты.

Django дополнительно проверяет:

```python
session.payment_status == "paid"
```

после чего меняет статус заказа:

```python
order.status = Order.Status.PAID
```

---

## 🔎 Поиск заказа

После успешной оплаты пользователь получает уникальный Order ID.

Например:

```text
DP-A72K91XF
```

Этот ID можно использовать на странице поиска заказов.

Пользователь вводит Order ID:

```text
/order/search/?order_id=DP-A72K91XF
```

После этого Django ищет соответствующий заказ в базе данных и отображает:

* Order ID
* Product
* Price
* Order status
* Order date

Если заказ не найден, отображается соответствующее сообщение.

---

## 🛠️ Технологии

### Backend

* Python
* Django
* Django ORM
* Class-Based Views (CBV)

### Database

* SQLite / PostgreSQL

### Payment

* Stripe Checkout
* Stripe API

### Frontend

* HTML5
* CSS3
* JavaScript
* Django Templates

### Environment

* Python `3.12+`
* `python-decouple`

---

## 📁 Структура проекта

```text
DrivePay/
│
├── apps/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── templates/
│   ├── home.html
│   ├── detail.html
│   ├── order.html
│   ├── success.html
│   └── cancel.html
│
├── root/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── manage.py
├── requirements.txt
└── .env
```

---

## 📦 Установка

Клонируйте репозиторий:

```bash
git clone <YOUR_REPOSITORY_URL>
cd DrivePay
```

Создайте виртуальное окружение:

```bash
python -m venv .venv
```

Активируйте его.

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Создайте файл `.env` в корне проекта:

```env
STRIPE_SK=sk_test_your_secret_key
STRIPE_PK=pk_test_your_publishable_key
```

**Не добавляйте `.env` в GitHub.**

Добавьте его в `.gitignore`:

```text
.env
.venv/
__pycache__/
db.sqlite3
```

---

## 🗄️ Database

Выполните миграции:

```bash
python manage.py makemigrations
python manage.py migrate
```

Для создания администратора:

```bash
python manage.py createsuperuser
```

---

## 👨‍💻 Django Admin

Административная панель доступна по адресу:

```text
/admin/
```

### Данные для входа

```text
Login: admin
Password: 1234
```

> ⚠️ Эти данные используются только для демонстрационного проекта. В production необходимо использовать сложный пароль и безопасную систему управления доступом.

Через Django Admin можно управлять:

* 🚗 автомобилями (`Item`)
* 📦 заказами (`Order`)
* 💳 статусами заказов
* 💰 ценами
* 📝 описаниями товаров

---

## ▶️ Запуск проекта

Запустите development server:

```bash
python manage.py runserver
```

После этого откройте:

```text
http://127.0.0.1:8000/
```

Админ-панель:

```text
http://127.0.0.1:8000/admin/
```

---

## 🧪 Stripe Test Mode

Проект использует Stripe в **Test/Sandbox Mode**.

Все платежи в тестовом режиме являются тестовыми и не списывают реальные деньги.

Для тестирования можно использовать тестовые банковские карты Stripe.

После завершения разработки Stripe можно переключить на **Live Mode**, заменив test API keys на live keys и настроив production environment.

---

## 📌 Order Status

Заказы проходят следующие состояния:

```text
PENDING
   ↓
Stripe Checkout
   ↓
Payment
   ↓
PAID
```

Если пользователь отменяет оплату:

```text
PENDING
   ↓
Cancel
```

Заказ при этом не считается оплаченным.

---

## 🔒 Безопасность

Секретный Stripe API key хранится в `.env`:

```python
stripe.api_key = config('STRIPE_SK')
```

Secret Key никогда не должен находиться непосредственно в GitHub-коде.

Для production рекомендуется дополнительно использовать:

* HTTPS
* PostgreSQL
* secure environment variables
* Stripe Webhooks
* CSRF protection
* secure cookies
* DEBUG=False
* ALLOWED_HOSTS
* production WSGI/ASGI server

---

## 🚀 Возможные улучшения

В следующих версиях проекта можно добавить:

* Stripe Webhooks
* Click
* Payme
* Telegram notifications
* Email notifications
* User authentication
* Order history
* Multiple products per order
* Cart
* Product images
* Search and filtering
* PostgreSQL
* Docker
* Nginx
* Production deployment

---

## 👨‍💻 Автор

**Hojimurod Kamolov**

Python / Django / Full-Stack Developer

Проект создан как практический проект для изучения:

```text
Django
+
Django ORM
+
CBV
+
Stripe API
+
Payment Processing
+
Order Management
```

---

## 📄 License

Проект создан в образовательных и демонстрационных целях.
