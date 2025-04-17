from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from users.views import (
    FavoriteListView,
    AddToFavoritesView,
    RemoveFromFavoritesView,
    ProfileView,
    SignUpView,
    ActivateAccountView,
)


urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="users/login.html"),
        name="login"),
    path(
        "logout/",
        LogoutView.as_view(next_page="main_page"),
        name="logout"
    ),
    path(
        "favorites/",
        FavoriteListView.as_view(),
        name="favorites"
    ),
    path(
        "product/<int:product_id>/add_to_favorites/",
        AddToFavoritesView.as_view(),
        name="add_to_favorites",
    ),
    path(
        "product/<int:product_id>/remove_from_favorites/",
        RemoveFromFavoritesView.as_view(),
        name="remove_from_favorites",
    ),
    path(
        "profile/",
        ProfileView.as_view(),
        name="profile"
    ),

    path(
        "signup/",
        SignUpView.as_view(),
        name="signup"
    ),
    path(
        "activate/<uidb64>/<token>/",
        ActivateAccountView.as_view(),
        name="activate"
    ),
    path(
        "",
        include("django.contrib.auth.urls")
    ),
]
