from src.dao import RedisDAO
from src.exceptions import PhoneNumberAlreadyExistsException, PhoneNumberNotExistException
from src.schemas import SPhoneData, SPhone
from src.utils.phone_number import validate_phone


class PhoneService:
    @staticmethod
    async def get_all_keys_and_values(dao: RedisDAO) -> list[dict]:
        keys = await dao.get_all_keys_and_values()
        return keys

    @staticmethod
    async def get(data: SPhone, dao: RedisDAO) -> dict:
        phone = data.phone
        checked_phone = validate_phone(phone)
        key = await dao.get_address_by_phone(checked_phone)
        return key

    @staticmethod
    async def add_phone(data: SPhoneData, dao: RedisDAO) -> None | dict:
        phone = data.phone
        address = data.address
        checked_phone = validate_phone(phone)

        if await dao.phone_exists(checked_phone):
            raise PhoneNumberAlreadyExistsException

        await dao.add_phone(checked_phone, address)
        return {"message": "Данные успешно сохранены", "phone": checked_phone, "address": address}

    @staticmethod
    async def update_address(data: SPhoneData, dao: RedisDAO) -> None | dict:
        phone = data.phone
        address = data.address
        checked_phone = validate_phone(phone)

        exist_phone = await dao.phone_exists(checked_phone)

        if not exist_phone:
            raise PhoneNumberNotExistException
        await dao.update_phone(checked_phone, address)
        return {"message": f"Данные успешно обновлены на: {address}"}


