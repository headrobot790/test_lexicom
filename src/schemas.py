from pydantic import BaseModel


class SPhoneDataRequest(BaseModel):
    phone: str
    address: str

    def __str__(self):
        return f"Phone: {self.phone}, Address: {self.address}"
