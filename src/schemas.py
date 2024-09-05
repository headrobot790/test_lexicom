from pydantic import BaseModel, Field, ConfigDict


class SPhoneData(BaseModel):
    phone: int
    address: str = Field(..., max_length=255)

    model_config = ConfigDict(from_attributes=True)

    def __str__(self):
        return f"Phone: {self.phone}, Address: {self.address}"
