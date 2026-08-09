# 🎬 Movie Ticket Booking & Community Review Portal

A Full Stack Django-based Movie Ticket Booking and Community Review Portal developed as a B.Tech Capstone Project.

---

## 📌 Project Overview

This project provides an online movie booking platform where users can browse movies, select showtimes, book seats interactively, and submit movie reviews.

The application is built using Django MVT architecture with Bootstrap 5, JavaScript, and SQLite.

---

## 🚀 Features

### 🎥 Movie Listing
- Display currently playing movies
- Search movies instantly
- Movie posters
- Ratings and vote count
- Genre and language information

### 🎟 Movie Details
- Movie synopsis
- Release date
- Duration
- Certificate
- Language
- Available showtimes
- Community reviews

### 💺 Interactive Seat Booking
- 5 × 8 JavaScript seat matrix
- Available seats
- Selected seats
- Booked seats
- Automatic ticket price calculation
- Booking confirmation ticket

### ⭐ Movie Reviews
- 5-Star rating system
- User comments
- Average movie rating
- Community review section

### 📱 Responsive UI
- Bootstrap 5
- Dark cinema theme
- Responsive movie cards
- Hover animations
- Mobile friendly

---

## 🛠 Technologies Used

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Font Awesome

### Backend

- Python
- Django
- Django ORM

### Database

- SQLite

### Deployment

- Render
- Gunicorn
- WhiteNoise

---

## 📂 Project Structure

```
movie_booking/
│
├── cinema/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py
│   └── migrations/
│
├── templates/
│   └── movies/
│       ├── home.html
│       ├── movie_detail.html
│       ├── booking.html
│       └── booking_success.html
│
├── static/
│   ├── style.css
│   ├── images/
│   └── js/
│
├── manage.py
├── requirements.txt
├── render.yaml
└── README.md
```

---

## 💻 Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into project

```bash
cd movie_booking
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run migrations

```bash
python manage.py migrate
```

Run server

```bash
python manage.py runserver
```

Open browser

```
http://127.0.0.1:8000/
```

---

## 🎯 Modules

- Movie Management
- Showtime Management
- Seat Booking
- Review System
- Booking Confirmation
- Search Movies

---

## 🔒 Security

- CSRF Protection
- Django Form Validation
- Duplicate Seat Prevention
- Atomic Booking Transactions

---

## ☁ Deployment

Configured for Render deployment with

- WhiteNoise
- Gunicorn
- render.yaml
- Automatic Superuser Creation

---

## 👩‍💻 Developed By

**Neha Dharavathu**

B.Tech Computer Science and Engineering

Velagapudi Ramakrishna Siddhartha Engineering College

---

## 📜 License

This project is developed for educational purposes as a B.Tech Capstone Project.
username:Nehaa
password:Arjunkittu