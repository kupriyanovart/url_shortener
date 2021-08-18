from django.urls import path, re_path

from url_shortener.views import CreateUrlView, redirect_view

app_name = "url_shortener"
urlpatterns = [
    path('', CreateUrlView.as_view(), name="index"),
    re_path(r"^(?P<hash_url>\w{10})$", redirect_view, name="redirect"),
]
