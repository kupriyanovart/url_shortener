from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


# Валидатор для формы UrlForm
def valid_url(value):
    url_validator = URLValidator()
    try:
        url_validator(value)
    except ValidationError:
        raise ValidationError("Некорректный URL! Пожалуйста, попробуйте еще раз!")
    return value


# Форма, используемая для ввода URL для сокращения
class UrlForm(forms.Form):
    url = forms.CharField(label='',
                          validators=[valid_url],
                          widget=forms.TextInput(attrs={"placeholder": "Введите URL",
                                                        "class": "form-control"}))
