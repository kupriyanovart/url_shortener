import hashlib

from django.conf import settings
from django.db import models


class Urls(models.Model):
    """
    Модель для хранения оригинального и короткого URL
    """
    class Meta:
        verbose_name = "Url"
        verbose_name_plural = "Urls"
    url = models.URLField(unique=True)
    hash_url = models.URLField(unique=True)

    def save(self, *args, **kwargs):
        self.hash_url = hashlib.sha256(self.url.encode()).hexdigest()[:10]
        return super().save(*args, **kwargs)

    def get_short_url(self):
        return settings.SITE_URL + "/" + self.hash_url
