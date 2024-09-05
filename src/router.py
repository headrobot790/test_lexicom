from fastapi import APIRouter, Depends

from src.dao import RedisDAO
from src.schemas import SPhoneData, SPhone
from src.service import PhoneService

phone_router = APIRouter(prefix="", tags=["Номера телефонов"])


@phone_router.get("/all_keys", response_model=list[SPhoneData])
async def get_all() -> list[dict]:
    """
    Получает все номера телефонов и адреса из базы Redis

    Пример запроса: http://127.0.0.1:8000/get_all
    """
    data = await PhoneService.get_all_keys_and_values(RedisDAO())
    return data


@phone_router.get("/check_data", response_model=SPhoneData)
async def check_data(data: SPhone = Depends()) -> dict:
    """
    Проводит проверку номера на валидность и получает адрес из базы Redis, если номер телефона существует.
    Если номера телефона не существует, то выбрасывается исключение

    Пример запроса: http://127.0.0.1:8000/check_data?phone=89991234567
    """
    data = await PhoneService.get(data, RedisDAO())
    return data


@phone_router.post("/write_data")
async def write_data(data: SPhoneData):
    """
    Проводит проверку номера на валидность и сохраняет данные (номер телефона и адрес) в базе Redis.
    Если номер телефона уже существует, то выбрасывается исключение

    Пример запроса: {phone: "89991234567", address: "Москва, ул. Пушкина, дом Колотушкина"}
    """
    data = await PhoneService.add_phone(data, RedisDAO())
    return data


@phone_router.put("/update_data")
async def update_data(data: SPhoneData):
    """
    Проводит проверку номера на валидность и обновляет данные (номер телефона и адрес) в базе Redis.
    Если номера телефона не существует, то выбрасывается исключение

    Пример запроса: {phone: "89991234567", address: "Москва, ул. Пушкина, дом Колотушкина"}
    """
    data = await PhoneService.update_address(data, RedisDAO())
    return data
