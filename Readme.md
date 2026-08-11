# 🌱 Seed2Sell — Farm-to-Table Marketplace

Seed2Sell is a Django-based agricultural marketplace that connects farmers
directly with buyers — no middlemen, no markups. Farmers list produce
straight from the field; customers browse, order, and check out, with the
platform handling everything from cart to payment to order tracking.

Built as a BCA final-year project (Gujarat University).

---

## ✨ Features

**Buyer side**
- Browse the marketplace with search, category filters, price filters, and sorting
- Product detail pages with farmer attribution
- Cart with live quantity updates
- Checkout with Cash-on-Delivery or UPI payment
- Order history and downloadable PDF invoices
- Customer dashboard

**Farmer side**
- Farmer dashboard with product & earnings overview
- Add / edit product listings (with images, category, price, unit)
- View incoming orders for their own products
- Track per-order earnings and payment status

**Platform**
- Custom user model with `farmer` / `customer` roles
- Session-based cart
- Role-aware authentication (single login/signup page, tabbed UI)

---

## 🛠 Tech Stack

- **Backend:** Django 5+ (Python)
- **Database:** SQLite (default, dev-ready — swap for Postgres/MySQL in production)
- **Frontend:** Django templates, Bootstrap 5, custom CSS design system (no JS framework)
- **PDF invoices:** ReportLab
- **Images:** Pillow

---

## ⚠️ Important note on payments

The UPI payment flow in this project is **simulated for demo purposes** —
there is no real payment gateway (Razorpay/Stripe/etc.) integrated. Cash on
Delivery orders are marked pending; UPI "payments" either auto-confirm or
resolve with a randomized success/failure, purely to demonstrate the full
order lifecycle (cart → checkout → payment → confirmation → order history).
Do not use this as-is for real transactions.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Setup

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd seed2sell

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. (Optional) Create an admin account
python manage.py createsuperuser

# 6. Run the dev server
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** in your browser.

### Trying it out
1. Go to **Login / Signup** and register as a **Farmer** — add a few products from the farmer dashboard.
2. Register a second account as a **Customer** — browse the marketplace, add items to cart, and check out.
3. Log back in as the farmer to see the order appear on the Orders page.

---

## 📁 Project Structure

```
seed2sell/
├── accounts/          # Custom user model, auth views
├── farmer/            # Core app: products, orders, cart, checkout, dashboards
├── templates/          # Django templates (global)
├── static/             # CSS, JS, images
├── media/              # User-uploaded product images (gitignored)
├── db.sqlite3          # Local dev database (gitignored)
└── manage.py
```

---

## 🔒 Before deploying anywhere public

This project is configured for **local development**:
- `DEBUG = True`
- `ALLOWED_HOSTS = ['*']`
- `SECRET_KEY` is hardcoded in `settings.py`

If you deploy this beyond a local demo, at minimum: move `SECRET_KEY` to an
environment variable, set `DEBUG = False`, restrict `ALLOWED_HOSTS`, and
switch to a production-grade database.

---

## 📄 License

Academic project — feel free to fork and learn from it.