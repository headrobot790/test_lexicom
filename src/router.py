import asyncio_redis as redis
from fastapi import HTTPException, APIRouter

from src.config import settings
from src.exceptions import PhoneNumberAlreadyExistsException, PhoneNumberNotExistsException
from src.schemas import SPhoneDataRequest
from src.utils.phone_number import validate_phone

phone_router = APIRouter(prefix="", tags=["Номера телефонов"])

redis_host, redis_port = settings.redis_host_port


async def get_redis_client():
    return await redis.Connection.create(host=redis_host, port=redis_port)


@phone_router.on_event("startup")
async def startup_event():
    global redis_client
    redis_client = await get_redis_client()


@phone_router.on_event("shutdown")
async def shutdown_event():
    global redis_client
    if redis_client:
        redis_client.close()
        await redis_client.wait_closed()


@phone_router.post("/write_data")
async def write_data(data: SPhoneDataRequest):
    """
    Проводит проверку номера на валидность и сохраняет данные (номер телефона и адрес) в базе Redis.
    Если номер телефона уже существует, то выбрасывается исключение

    Пример запроса: {phone: "89991234567", address: "Москва, ул. Пушкина, дом Колотушкина"}
    """
    phone = validate_phone(data.phone)

    exist_phone = await redis_client.exists(phone)
    if not exist_phone:
        await redis_client.set(phone, data.address)
        return {"message": "Данные успешно сохранены"}
    else:
        raise PhoneNumberAlreadyExistsException


@phone_router.put("/write_data")
async def write_data(data: SPhoneDataRequest):
    """
    Проводит проверку номера на валидность и обновляет данные (номер телефона и адрес) в базе Redis.
    Если номера телефона не существует, то выбрасывается исключение

    Пример запроса: {phone: "89991234567", address: "Москва, ул. Пушкина, дом Колотушкина"}
    """
    phone = validate_phone(data.phone)
    exist_phone = await redis_client.exists(phone)
    if exist_phone:
        await redis_client.set(phone, data.address)
        return {"message": "Данные успешно обновлены"}
    else:
        raise PhoneNumberNotExistsException


@phone_router.get("/check_data")
async def check_data(phone: str):
    """
    Проводит проверку номера на валидность и получает адрес из базы Redis, если номер телефона существует.
    Если номера телефона не существует, то выбрасывается исключение

    Пример запроса: http://127.0.0.1:8000/check_data?phone=89991234567
    """
    phone = validate_phone(phone)
    try:
        address = await redis_client.get(phone)
        if address:
            return {"phone": phone, "address": address}
        else:
            raise PhoneNumberNotExistsException
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
