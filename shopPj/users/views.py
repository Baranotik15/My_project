import logging
import threading

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


from users.services.token_service import account_activation_token
from users.forms import CustomUserCreationForm
from orders.models import Order
from products.models import Product


logger = logging.getLogger(__name__)


class FavoriteListView(LoginRequiredMixin, ListView):
    template_name = "users/favorites.html"
    context_object_name = "favorites"

    def get_queryset(self):
        return Product.objects.filter(favorite_products=self.request.user)


class AddToFavoritesView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        request.user.favorite_products.add(product)
        return redirect("product_detail", pk=product.id)


class RemoveFromFavoritesView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)

        if product in request.user.favorite_products.all():
            request.user.favorite_products.remove(product)
            return redirect("favorites")
        else:
            return redirect("product_detail", pk=product.id)


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        orders = Order.objects.filter(user=user).order_by("-created_at")

        orders_with_details = []
        for order in orders:
            order_items = order.order_items.all()
            total_price = (
                order.total_price
                if hasattr(order, "total_price")
                else sum(
                    item.quantity * item.product.price
                    for item in order_items
                )
            )
            orders_with_details.append(
                {
                    "order": order,
                    "order_items": order_items,
                    "total_price": total_price
                }
            )

        return render(
            request,
            "users/profile.html",
            {
                "user": user,
                "orders": orders_with_details,
            },
        )


class SignUpView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = CustomUserCreationForm()

        return render(request, "users/signup.html", {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CustomUserCreationForm(request.POST)

        if not form.is_valid():
            return render(request, "users/signup.html", {"form": form})

        try:
            with transaction.atomic():
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                current_site = get_current_site(request)
                mail_subject = "Activate your account."
                message = render_to_string(
                    "users/emails/acc_active_email.html",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": account_activation_token.make_token(user),
                    },
                )
                email = EmailMessage(mail_subject, message, to=[user.email])
                email.content_subtype = "html"

                threading.Thread(target=email.send).start()
        except Exception as e:
            logging.error(f"Error sending email: {e}")

            return render(request, "users/signup.html", {"form": form})

        return render(request, "users/email_confirmation_sent.html")


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(
                request,
                "Thank you for confirming your email. You can now login to your account.",
            )
            return redirect("accounts:login")
        else:
            return render(request, "users/activation_invalid.html")
