import re
from fastapi import Query

from src.exceptions import IncorrectPhoneNumberFormatException

phone_pattern_ru = re.compile(r'^(?:7|8)\d{10}$')


def validate_phone(phone: int = Query(..., description="Номер телефона")):
    phone = str(phone)
    if not phone_pattern_ru.match(phone):
        raise IncorrectPhoneNumberFormatException
    normalized_phone = '8' + phone[-10:]
    return normalized_phone
