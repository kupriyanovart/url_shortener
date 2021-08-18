from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def valid_url(value):
    """
    Валидатор для формы UrlForm
    """
    url_validator = URLValidator()
    try:
        url_validator(value)
    except ValidationError:
        raise ValidationError("Некорректный URL! Пожалуйста, попробуйте еще раз!")
    return value


class UrlForm(forms.Form):
    """
    Форма, используемая для ввода URL для сокращения
    """
    url = forms.CharField(
        label="",
        validators=[valid_url],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите URL",
                "class": "form-control"
            }
        )
    )
