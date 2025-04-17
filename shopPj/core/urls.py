from django.urls import path
from core.views import Home, AboutView

urlpatterns = [
    path("", Home.as_view(), name="main_page"),
    path("about/", AboutView.as_view(), name="about"),
]
