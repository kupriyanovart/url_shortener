import hashlib
from urllib.parse import urlencode

from django.test import TestCase
from django.urls import reverse

from .forms import UrlForm
from .models import Urls


class UrlFormTest(TestCase):
    """
    Тестирование формы
    """

    def test_form_valid_url(self):
        url = "https://yandex.ru/"
        form_data = {"url": url}
        form = UrlForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_url(self):
        url = "yandex.ru"
        form_data = {"url": url}
        form = UrlForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_url_2(self):
        url = "https://yandex .ru/"
        form_data = {"url": url}
        form = UrlForm(data=form_data)
        self.assertFalse(form.is_valid())


class ModelTest(TestCase):
    """
    Тестирование модели
    """

    @classmethod
    def setUpTestData(cls):
        """Создание объекта, используемого в остальных методах"""
        Urls.objects.create(url="https://yandex.ru/")

    def test_create_db_record(self):
        db_record = Urls.objects.get(id=1)
        hash_url = hashlib.sha256(db_record.url.encode()).hexdigest()[:10]
        self.assertTrue(hash_url == db_record.hash_url)


class CreateViewTest(TestCase):
    """
    Тестирование отображения CreateView
    """
    @classmethod
    def setUpTestData(cls):
        """Создание объекта, используемого в остальных методах"""
        Urls.objects.create(url="https://yandex.ru/")

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get("")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("url_shortener:index"))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse("url_shortener:index"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "url_shortener/urls_create.html")

    def test_view_create_new_db_record(self):
        """Создание новой записи в БД"""
        url = "https://google.ru/"
        form_data = {"url": url}
        data = urlencode(form_data)
        resp = self.client.post('/', data=data, content_type="application/x-www-form-urlencoded")
        db_record = Urls.objects.get(url="https://google.ru/")
        self.assertEqual(url, db_record.url)
        self.assertTrue(db_record.hash_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "url_shortener/urls_success.html")

    def test_view_create_submit_existed_url(self):
        """Ввод в форму уже существующий в БД URL"""
        url = "https://yandex.ru/"
        form_data = {"url": url}
        data = urlencode(form_data)
        resp = self.client.post('/', data=data, content_type="application/x-www-form-urlencoded")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "url_shortener/urls_success.html")


class RedirectViewTest(TestCase):
    """Тестирование отображения redirect_view"""
    @classmethod
    def setUpTestData(cls):
        """Создание объекта, используемого в остальных методах"""
        Urls.objects.create(url="https://yandex.ru/")

    def test_view_redirect(self):
        record = Urls.objects.get(pk=1)
        resp = self.client.get(reverse("url_shortener:redirect", args=[record.hash_url]))
        self.assertRedirects(
            resp,
            expected_url="https://yandex.ru/",
            fetch_redirect_response=False  # Тест не загружает страницу на которую перенаправляет
        )
