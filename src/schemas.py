from pydantic import BaseModel, Field, ConfigDict


class PhoneArgs:
    def __init__(self, phone: int):
        self.phone = phone


class SPhone(BaseModel):
    phone: int = Field(ge=70000000000, le=89999999999)

    model_config = ConfigDict(from_attributes=True)

    def __str__(self):
        return f"Phone: {self.phone}"


class SPhoneData(SPhone):
    address: str = Field(..., max_length=255)

    model_config = ConfigDict(from_attributes=True)

    def __str__(self):
        return f"Phone: {self.phone}, Address: {self.address}"
