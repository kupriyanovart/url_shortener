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
