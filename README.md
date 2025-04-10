# Online Clothing Store

Это стандартный интернет-магазин одежды, разработанный с использованием Django. Пользователи могут просматривать каталог товаров, добавлять их в корзину, оформлять заказы и оплачивать через Stripe.
Реализована регистрация и авторизация с подтверждением по электронной почте, а также админ-панель для управления товарами.

## Функционал

- Просмотр списка товаров
- Детальный просмотр товара
- Добавление товаров в корзину
- Добавление товара в избранное
- Оформление заказа
- Оплата через Stripe
- Регистрация и авторизация пользователей с подтверждением на почту
- Админ-панель для добавления и обновления товаров

## Используемые технологии

- **Django 5.1.7** — основной фреймворк
- **SQLite** — база данных (для разработки; для production рекомендуется PostgreSQL)
- **Stripe 12.0.0** — для обработки платежей
- **Dropbox** — для хранения изображений товаров

![Untitled](https://github.com/user-attachments/assets/e7b6f166-d64d-4918-8d95-72f3cf900144)


https://dbdiagram.io/d/67e326df75d75cc84473f67f
  
## Установка и запуск

1. Клонируйте репозиторий:

   - **SSH:**

     ```
     git clone git@github.com:Baranotik15/My_project.git
     ```

   - **HTTPS:**

     ```
     git clone https://github.com/Baranotik15/My_project.git
     ```

3. Установите зависимости:
   pip install -r requirements.txt

4. Настройте файл `.env` с необходимыми переменными окружения (смотрите раздел Конфигурации)

5. Примените миграции:
   python manage.py migrate

6. Запустите сервер:
   python manage.py runserver



## Конфигурация

Для работы приложения необходимо создать файл `.env` в корневой директории проекта и указать следующие переменные окружения:

- `SECRET_KEY` — секретный ключ Django (например, сгенерируйте через `django.core.management.utils.get_random_secret_key()`)
- `DEBUG` — `True` для разработки, `False` для production
- `STRIPE_PUBLIC_KEY` — публичный ключ Stripe
- `STRIPE_SECRET_KEY` — секретный ключ Stripe
- `DROPBOX_APP_KEY` — ключ приложения Dropbox
- `DROPBOX_APP_SECRET` — секретный ключ приложения Dropbox
- `DROPBOX_ACCESS_TOKEN` — токен доступа Dropbox
- `EMAIL_HOST` — хост почтового сервера (например, `smtp.gmail.com`)
- `EMAIL_PORT` — порт почтового сервера (например, `587`)
- `EMAIL_HOST_USER` — пользователь почтового сервера (например, ваш email)
- `EMAIL_HOST_PASSWORD` — пароль почтового сервера
- `DEFAULT_FROM_EMAIL` — email, с которого отправляются письма (например, `your.email@gmail.com`)

Пример файла `.env`:
```
  SECRET_KEY=your_django_secret_key
  DEBUG=True
  STRIPE_PUBLIC_KEY=pk_test_yourstripepublickey
  STRIPE_SECRET_KEY=sk_test_yourstripesecretkey
  DROPBOX_APP_KEY=your_dropbox_app_key
  DROPBOX_APP_SECRET=your_dropbox_app_secret
  DROPBOX_ACCESS_TOKEN=your_dropbox_access_token
  EMAIL_HOST=smtp.gmail.com
  EMAIL_PORT=587
  EMAIL_HOST_USER=your.email@gmail.com
  EMAIL_HOST_PASSWORD=your_email_password
  DEFAULT_FROM_EMAIL=your.email@gmail.com
```

## Лицензия
ToDo



