from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="main_page"),
    path("about/", views.AboutView.as_view(), name="about"),
]
