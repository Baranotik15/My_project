from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="main_page"),
    path("about/", views.AboutView.as_view(), name="about"),
]
