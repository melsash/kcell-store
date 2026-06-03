# Kcell Store

Online store developed with FastAPI, PostgreSQL, SQLAlchemy, Jinja2 Templates and Docker.

## Project Description

Kcell Store is a web application that simulates a modern online electronics store. Users can browse products, search items, filter by category, add products to a shopping cart, place orders, and select a payment method during checkout.

The project was developed as part of the Kcell Internship selection process.

---

## Features

### Customer Features

* Product catalog
* Product details page
* Product search
* Product category filtering
* Product price sorting
* Shopping cart
* Quantity management in cart
* Checkout page
* Order creation
* Payment method selection
* Order success page

### Authentication

* User registration
* User login
* User logout
* Session-based authentication

### Admin Features

* Admin role support
* Admin panel
* Product management
* Order management
* User management

---

## Product Categories

The application supports multiple product categories:

* Smartphone
* Tablet
* Audio
* Wearable

Users can filter products by category directly from the shop page.

---

## Payment Methods

The checkout process supports multiple payment methods:

* Kaspi
* Visa / MasterCard
* Cash on Delivery

The selected payment method is stored with the order.

---

## Order Status

Each order automatically receives a status.

Current statuses:

* Pending (default)

The status is stored in the database and can be extended in future versions.

---

## Technologies Used

Backend:

* Python 3.12
* FastAPI
* SQLAlchemy
* PostgreSQL

Frontend:

* HTML
* CSS
* Jinja2 Templates

Infrastructure:

* Docker
* Docker Compose

---

## Database Models

### User

* id
* email
* password
* role

### Product

* id
* name
* description
* price
* image
* category

### Order

* id
* customer_name
* phone_number
* payment_method
* status
* user_id
* created_at

### OrderItem

* id
* order_id
* product_id
* quantity

---

## Admin Credentials

Default Admin Account

Email: admin@kcell.store
Password: Admin123!

The account is automatically created during application startup.
---

## Installation

Clone repository:

git clone https://github.com/melsash/kcell-store.git

Open project folder:

cd kcell-store

Run application:

docker compose up --build

---

## Application URL

Store:

http://localhost:8000/shop

Swagger API Documentation:

http://localhost:8000/docs

---

## Future Improvements

* Online payment gateway integration
* Order status management from admin panel
* Product image upload
* Product reviews and ratings
* Email notifications
* User profile page

---


## Author

Ash

Kcell Internship Project
