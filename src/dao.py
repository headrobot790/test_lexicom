from redis import asyncio as aioredis

from src.exceptions import PhoneNumberNotExistException, PhoneNumberAlreadyExistsException
from src.schemas import SPhoneData
from src.utils.phone_number import validate_phone


class RedisDAO:
    @classmethod
    async def phone_exists(cls, phone: str) -> bool:
        async with aioredis.Redis(decode_responses=True) as request:
            return await request.exists(phone)

    @classmethod
    async def get_all_keys_and_values(cls) -> list[dict]:
        async with aioredis.Redis(decode_responses=True) as request:
            keys = await request.keys()
            data = []
            for key in keys:
                value = await request.get(key)
                if value:
                    data.append({"phone": int(key), "address": value})
            return data

    @classmethod
    async def get_address_by_phone(cls, phone: int) -> dict:
        async with aioredis.Redis(decode_responses=True) as request:
            phone = validate_phone(phone)
            address = await request.get(phone)
            if address:
                data = {"phone": phone, "address": address}
            else:
                raise PhoneNumberNotExistException
            return data

    @classmethod
    async def add_phone(cls, phone: str, address: str):
        async with aioredis.Redis(decode_responses=True) as request:
            await request.set(phone, address)

    @classmethod
    async def update_phone(cls, phone: str, address: str):
        async with aioredis.Redis(decode_responses=True) as request:
            await request.set(phone, address)

