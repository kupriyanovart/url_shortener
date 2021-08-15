import hashlib

from django.conf import settings
from django.db import models
from django.urls import reverse

SITE_URL = getattr(settings, "SITE_URL", 'http://127.0.0.1:8000')


# Модель для хранения оригинального и короткого URL
class Urls(models.Model):
    class Meta:
        verbose_name = "Url"
        verbose_name_plural = "Urls"
    url = models.URLField(unique=True)
    hash_url = models.URLField(unique=True)

    def save(self, *args, **kwargs):
        self.hash_url = hashlib.sha256(self.url.encode()).hexdigest()[:10]
        return super().save(*args, **kwargs)

    def get_short_url(self):
        url_path = reverse(viewname='url_shortener:redirect', kwargs={'hash_url': self.hash_url})
        url_path = SITE_URL+url_path
        return url_path
