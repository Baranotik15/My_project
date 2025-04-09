import threading

from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.services.token_service import account_activation_token

User = get_user_model()


class UserService:

    @classmethod
    def create_user(
        cls,
        username: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        domain: str,
        **kwargs
    ):
        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=False,
            )
            user.save()

            mail_subject = "Activate your account."
            message = render_to_string(
                "users/emails/acc_active_email.html",
                {
                    "user": user,
                    "domain": domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.content_subtype = "html"

            threading.Thread(target=email.send).start()

            return user
