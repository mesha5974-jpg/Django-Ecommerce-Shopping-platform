# Django Ecommerce Shopping Platform

A web-based ecommerce shopping application developed using **Python and Django**. This project provides an online shopping experience with product browsing, category management, user authentication, shopping cart functionality, checkout, order history, and inventory management.

**Repository:** [Django-Ecommerce-Shopping-platform](https://github.com/mesha5974-jpg/Django-Ecommerce-Shopping-platform)

## Features

### User Authentication
- User registration
- User login and logout
- Email-based login

### Product Management
- Browse available products
- View product details
- Organize products into categories
- Add, edit, and delete products through authorized admin functionality

### Shopping Cart
- Add products to the cart
- Update product quantities
- Remove products from the cart

### Checkout and Orders
- Checkout and order placement
- Cash on Delivery (COD)
- View order history
- Manage order statuses

### Inventory Management
- Track product stock
- Manage product availability

### Email Notifications
- Email notifications for supported order-related events

## Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS
- **Database:** SQLite
- **Version Control:** Git and GitHub

## Project Structure

```text
Django-Ecommerce-Shopping-platform/
├── ecom/
├── ecommerce/
├── media/
│   └── photos/
├── static/
│   └── css/
├── templates/
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## Getting Started

Follow these steps to set up the project locally.

### Prerequisites

- Python installed on your computer
- Git installed on your computer

### 1. Clone the Repository

```bash
git clone https://github.com/mesha5974-jpg/Django-Ecommerce-Shopping-platform.git
cd Django-Ecommerce-Shopping-platform
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```bat
venv\Scripts\activate.bat
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure Environment Variables

If the project settings use environment variables, create a `.env` file in the project root, alongside `manage.py`.

Add the variables required by `ecommerce/settings.py`. For example:

```dotenv
SECRET_KEY=replace-with-your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-app-password
```

Use your own values and ensure the variable names match the project's settings. Email configuration is required only if email notifications use SMTP.

**Security:** Never commit your `.env` file, passwords, or secret keys to GitHub.

### 6. Apply Database Migrations

```bash
python manage.py migrate
```

### 7. Create an Administrator Account

To create a Django administrator account, run:

```bash
python manage.py createsuperuser
```

Follow the prompts to configure the account.

### 8. Start the Development Server

```bash
python manage.py runserver
```

Open the following URL in your browser:

http://127.0.0.1:8000/

## Configuration Notes

- SQLite is configured for local development.
- Product images use Django's media functionality.
- Email notifications depend on the project's email configuration.
- A fresh database may require product categories and products to be created before the shopping workflow can be tested.
- If uploaded images are not included in the repository, add product images locally as needed.

## Security

- Keep secret keys and email credentials private.
- Do not upload `.env` files or other sensitive configuration to GitHub.
- Use `DEBUG=False` and configure appropriate `ALLOWED_HOSTS` before production deployment.
- Review database, media, and static-file handling before deploying the application publicly.

## Project Status

A Django ecommerce project developed to practice web development, database management, authentication, shopping cart operations, checkout, and order management.

## Author

**Esha Arshad**

GitHub: [@mesha5974-jpg](https://github.com/mesha5974-jpg)

## License

No license has been specified for this repository. All rights are reserved by default unless the author provides a license. Contact the repository owner for permission to reuse or redistribute the code.
