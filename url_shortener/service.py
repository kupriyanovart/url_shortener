import hashlib
import json

from django.conf import settings

from url_shortener.models import Urls


class HashMaker:
    def __init__(self, url):
        self.url = url

    def generate(self):
        return hashlib.sha256(self.url.encode()).hexdigest()[:10]


class CreateShortUrlService:

    def __init__(self, url):
        self.url = url

    def create_hash(self):
        hash_maker = HashMaker(self.url)
        hash_code = hash_maker.generate()
        return hash_code

    def create_short_url(self):
        return settings.SITE_URL + "/" + self.create_hash()

    def _save_url(self):
        obj, _ = Urls.objects.get_or_create(url=self.url, hash_url=self.create_hash())

    def get_url_and_short_url(self):
        self._save_url()
        result = {
            "url": self.url,
            "short_url": self.create_short_url(),
        }
        return json.dumps(result, ensure_ascii=False)


class MainPageService:
    @staticmethod
    def get_context():
        context = {
            "title": "Сокращатель ссылок 3000",
        }
        return json.dumps(context, ensure_ascii=False)


class RedirectFromShortUrlService:
    def __init__(self, hash_url):
        self.hash_url = hash_url

    def get_original_url(self):
        original_url = Urls.objects.get(hash_url=self.hash_url)
        return original_url.url
