import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    year_today = datetime.date.today().year
    if value > year_today:
        raise ValidationError(("Год произведения не может быть в будущем"))
    return value
