from fastapi import HTTPException, status


PhoneNumberAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Телефон уже существует",
)

PhoneNumberNotExistsException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Номер не найден"
)

IncorrectPhoneNumberFormatException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Некорректный номер телефона. Он должен начинаться с +7, 7 или 8 и содержать 10 цифр после этого."
)
