from django.http import Http404, HttpResponse
from django.http import HttpResponseRedirect
from django.views import View

from .forms import UrlForm
from .service import CreateShortUrlService, MainPageService, RedirectFromShortUrlService


class CreateUrlView(View):
    def get(self, request, *args, **kwargs):
        service = MainPageService()
        context = service.get_context()
        response = HttpResponse(context, content_type="application/json", *args, **kwargs)
        return response

    def post(self, request, *args, **kwargs):
        form = UrlForm(request.POST)
        print(request.method)
        if form.is_valid():
            url = form.cleaned_data.get("url")
            service = CreateShortUrlService(url)
            context = service.get_url_and_short_url()
            response = HttpResponse(context, content_type="application/json")
            return response
        return HttpResponseRedirect("/")


def redirect_view(request, hash_url=None, *args, **kwargs):
    try:
        service = RedirectFromShortUrlService(hash_url)
        print(service.get_original_url())
        return HttpResponseRedirect(service.get_original_url())
    except Http404:
        return HttpResponseRedirect("/")
