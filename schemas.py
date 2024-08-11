from pydantic import BaseModel, Field
from typing import Optional
from pydantic.networks import EmailStr
from pydantic.types import SecretStr, constr


class UserLogin(BaseModel):
    username_or_email: str
    password: str


class UserRegister(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    username: constr(to_lower=True)
    email: EmailStr
    password: str
    telephone_number: str
    region: str
    is_admin: Optional[bool] = False
    is_verified: Optional[bool] = False

    class Config:
        from_attributes = True
        orm_mode = True
        schema_extra = {
            'example': {
                "first_name": "John",
                "last_name": "Doe",
                "username": 'john_doe03',
                "email": 'john_doe@example.com',
                "password": 'secret_key',
                "telephone_number": "+99899123466",
                "region": "Uzbekistan",
                "is_admin": False,
                "is_verified": False
            }
        }


class User(UserRegister):
    passport_image: Optional[str] = None


class Settings(BaseModel):
    authjwt_secret_key: str = "130635b03885a6ac0553571d742399f1afa33f07307a3380127564ea8bd73dd0"


