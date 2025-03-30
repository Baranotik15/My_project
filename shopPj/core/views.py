from django.shortcuts import render
from django.views.generic import TemplateView

from products.models import Category


def home(request):
    categories = Category.objects.all()
    return render(request, "core/home.html", {"categories": categories})


class AboutView(TemplateView):
    template_name = "core/about.html"
