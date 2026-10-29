
# Django Ecommerce Shopping Website

A web-based ecommerce shopping application developed using Django and Python. Users can browse products, view product details, add items to their cart, and place orders.

## Features

- User registration and login
- Product listing and category management
- Product details with images
- Shopping cart functionality
- Order placement and order history
- Order status management
- Admin product management
- Stock management
- Email notifications

## Technologies Used

- Python
- Django
- HTML
- CSS
- SQLite
- Git and GitHub

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd YOUR_PROJECT_FOLDER
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root and configure the required settings, including `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and email credentials.

Do not upload your `.env` file to GitHub.

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Project Status

This project is being developed as a Django ecommerce application.

## Author

Esha Arshad
