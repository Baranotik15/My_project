# Online Clothing Store

This is a standard online clothing store developed using Django. Users can browse the product catalog, add items to the cart, place orders, and pay via Stripe.  
User registration and authentication with email confirmation are implemented, along with an admin panel for managing products.

## Features

- Browse product listings  
- View detailed product pages  
- Add items to the cart  
- Add items to favorites  
- Place orders  
- Payment via Stripe  
- User registration and login with email confirmation  
- Admin panel for adding and updating products  

## Technologies Used

- **Django 5.1.7** — main framework  
- **SQLite** — database (used for development; PostgreSQL is recommended for production)  
- **Stripe 12.0.0** — for payment processing  
- **Dropbox** — for storing product images  

## DB Model Diagram
![Untitled](https://github.com/user-attachments/assets/e7b6f166-d64d-4918-8d95-72f3cf900144)

https://dbdiagram.io/d/67e326df75d75cc84473f67f

## Installation and Setup

1. Clone the repository:

   - **SSH:**

     ```
     git clone git@github.com:Baranotik15/My_project.git
     ```

   - **HTTPS:**

     ```
     git clone https://github.com/Baranotik15/My_project.git
     ```

2. Install dependencies:  
   ```
   pip install -r requirements.txt
   ```

3. Configure the `.env` file with the required environment variables (see Configuration section)

4. Apply migrations:  
   ```
   python manage.py migrate
   ```

5. Run the server:  
   ```
   python manage.py runserver
   ```

## Configuration

To run the application, create a `.env` file in the root directory of the project and specify the following environment variables:

- `SECRET_KEY` — Django secret key (you can generate one using `django.core.management.utils.get_random_secret_key()`)  
- `DEBUG` — `True` for development, `False` for production  
____
- `STRIPE_PUBLIC_KEY` — your Stripe public key   (You can found info here: https://docs.stripe.com/keys)
- `STRIPE_SECRET_KEY` — your Stripe secret key
____
- `DROPBOX_APP_KEY` — your Dropbox app key  (You can do it here: https://www.dropbox.com/developers/apps/create)
- `DROPBOX_APP_SECRET` — your Dropbox app secret  
- `DROPBOX_ACCESS_TOKEN` — your Dropbox access token
- ____
- `EMAIL_HOST` — email host (e.g., if gmail `smtp.gmail.com`)  
- `EMAIL_PORT` — email port (e.g., if TLS `587` else if SSL `465`)  
- `EMAIL_HOST_USER` — email host user (e.g., your email)  
- `EMAIL_HOST_PASSWORD` — email host password (need on two-factor authentication)
- `DEFAULT_FROM_EMAIL` — the email address from which emails will be sent (e.g., `your.email@gmail.com`)  
____

Example `.env` file (.env.sample):
```
# DB
POSTGRES_DB=
POSTGRES_DB_PORT=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=

# Django
SECRET_KEY=c3kItd4jbqdIwrUOc6A4h1c7Yy7P0S
DJANGO_SETTINGS_MODULE=confit.settings.dev

# DropBox
DROPBOX_APP_KEY=
DROPBOX_APP_SECRET=
DROPBOX_OAUTH2_REFRESH_TOKEN=

#Stripe
STRIPE_PUBLIC_KEY=
STRIPE_SECRET_KEY=

#Email
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=
```
## SITE EXEMPLE:
-  https://shop-store-scissors.onrender.com