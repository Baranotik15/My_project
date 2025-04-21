import logging

from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.services.email_service import send_activation_email


from users.services.token_service import account_activation_token
from users.forms import CustomUserCreationForm, CustomLoginForm
from orders.models import Order
from products.models import Product


logger = logging.getLogger(__name__)
User = get_user_model()


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


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'users/login.html'


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

                send_activation_email(request, user)

        except Exception as e:
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
                "Спасибо за подтверждение email. Теперь вы можете войти в ваш аккаунт.",
            )
            return redirect("login")
        else:
            return render(request, "users/activation_invalid.html")
