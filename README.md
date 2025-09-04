# CS50W Project 2 — Commerce (Auctions)

An eBay-like auction site built with Django. Users can create listings, place bids, comment, manage a watchlist, browse by categories, and close auctions. This repository contains only the required files for submission: `auctions/`, `commerce/`, and `manage.py`.

> Demo video: _(add your YouTube link here)_

## Features

- **User accounts** (register, login, logout)
- **Create listing** with title, description, starting bid, optional image URL, and optional category
- **Active listings page** showing title, description, current price, and photo
- **Listing page**
  - Place bids (must be ≥ starting bid and greater than current highest)
  - Add/remove from **Watchlist**
  - **Close auction** (owner only) → highest bidder becomes winner
  - Winner sees **“You won this auction!”** on the closed listing
  - Add and view **comments**
- **Watchlist page** for signed-in users
- **Categories** list and category-specific active listings
- **Django Admin** to view/add/edit/delete users, listings, bids, and comments

## Tech Stack

- Python 3.x, Django 5
- SQLite (default dev database)
- HTML/CSS (no frontend framework required by spec)

## Getting Started

> You only need the three items at the repo root: `auctions/`, `commerce/`, `manage.py`.

```bash
# 1) Clone
git clone https://github.com/Derrick-Chun/cs50-commerce.git
cd cs50-commerce

# 2) Checkout the project branch (used for CS50 submissions)
git checkout web50/projects/2020/x/commerce

# 3) (Optional but recommended) Create a virtual env
python3 -m venv venv
source venv/bin/activate

# 4) Install Django (project uses Django 5; any recent 5.x is fine)
pip install "Django>=5,<6"

# 5) Migrate database
python manage.py migrate

# 6) (Optional) Create an admin/superuser to use /admin
python manage.py createsuperuser

# 7) Run
python manage.py runserver
