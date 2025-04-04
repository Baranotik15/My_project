from django.shortcuts import render
from django.views.generic import TemplateView, View

from products.models import Category


class Home(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()

        return render(
            request,
            "core/home.html",
            {"categories": categories}
        )


class AboutView(TemplateView):
    template_name = "core/about.html"
