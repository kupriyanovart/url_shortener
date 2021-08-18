from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import UrlForm
from .models import Urls


class CreateUrlView(View):
    def get(self, request, *args, **kwargs):
        form = UrlForm()
        context = {
            "title": "Сокращатель ссылок 3000",
            "form": form
        }
        return render(request, "url_shortener/urls_create.html", context)

    def post(self, request, *args, **kwargs):
        form = UrlForm(request.POST)
        context = {
            "title": "Submit URL",
            "form": form
        }
        if form.is_valid():
            current_url = form.cleaned_data.get("url")
            obj, created = Urls.objects.get_or_create(url=current_url)
            context = {
                "title": "Ссылка сокращена!",
                "object": obj,
                "created": created
            }
            return render(request, "url_shortener/urls_success.html", context)
        return render(request, "url_shortener/urls_create.html", context)


def redirect_view(request, hash_url=None, *args, **kwargs):
    try:
        obj = Urls.objects.get(hash_url=hash_url)
        return HttpResponseRedirect(obj.url)
    except Http404:
        return render(request, "url_shortener/urls_create.html")
