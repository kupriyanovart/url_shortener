import hashlib

from django.db import models


class Urls(models.Model):
    class Meta:
        verbose_name = "Url"
        verbose_name_plural = "Urls"
    url = models.URLField(unique=True)
    hash_url = models.URLField(unique=True)

    def save(self, *args, **kwargs):
        self.hash_url = hashlib.sha256(self.url.encode()).hexdigest()[:10]
        return super().save(*args, **kwargs)
