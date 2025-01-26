from pydantic import BaseModel, SecretStr, EmailStr
from pydantic.types import constr


class UserInput(BaseModel):
    email: EmailStr
    password: SecretStr


class UserOutput(BaseModel):
    email: EmailStr
    full_name: str
    phone_number: constr(regex=r'^\+?1?\d{9,15}$')
    address: str


class TokenOutput(BaseModel):
    access_token: str
    token_type: str
