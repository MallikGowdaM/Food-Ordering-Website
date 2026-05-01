# FoodieHub 🍔 — Online Food Ordering System

A full-stack food ordering web app built with **Django 6**, **Bootstrap 5**, and **SQLite**.

## Tech Stack
- **Backend:** Python / Django 6
- **Frontend:** HTML, CSS, Bootstrap 5
- **Database:** SQLite (default Django)
- **Auth:** Django built-in authentication

## Features
- User registration & login
- Browse food menu with category filters
- Add to cart, update quantities, remove items
- Checkout with delivery address & phone
- Order history with status tracking
- Django Admin panel for managing food items & orders

## Quick Start

```bash
# 1. Install dependencies
python -m pip install django pillow

# 2. Apply migrations
python manage.py migrate

# 3. Load sample food data
python manage.py seed_data

# 4. Create admin account
python manage.py createsuperuser

# 5. Run the server
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

Admin panel: **http://127.0.0.1:8000/admin/**

## Pages

| Page | URL |
|------|-----|
| Home | `/` |
| Menu | `/menu/` |
| Register | `/register/` |
| Login | `/login/` |
| Cart | `/cart/` |
| Checkout | `/checkout/` |
| Order History | `/orders/` |
| Admin Panel | `/admin/` |
