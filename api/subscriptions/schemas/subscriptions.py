from pydantic import BaseModel, Field, EmailStr
from beanie import Document


class Subscription(Document):
    name: str = Field(...)
    number: str = Field(...)
    mail: EmailStr = Field(...)

    class Settings:
        name = "subscription"

    class Config:
        schema_extra = {
            "example": {
                "name": "Abdulazeez",
                "number": "+58-000000000",
                "mail": "mail@mail.com",
            }
        }
