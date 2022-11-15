from pydantic import BaseModel, Field, EmailStr
from beanie import Document


class Subscription(Document):
    name: str = Field(...)
    last_name: str = Field(...)
    cedula: str = Field(...)
    phone: str = Field(...)
    mail: EmailStr = Field(...)

    class Settings:
        name = "subscription"

    class Config:
        schema_extra = {
            "example": {
                "name": "Mario",
                "last_name": "Castro",
                "cedula": "12456789",
                "phone": "+58-000000000",
                "mail": "mail@mail.com",
            }
        }
