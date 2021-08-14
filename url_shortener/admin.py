from django.contrib import admin

from .models import Urls


class UrlsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Urls, UrlsAdmin)

