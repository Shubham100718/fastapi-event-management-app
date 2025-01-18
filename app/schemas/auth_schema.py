import re
from pydantic import BaseModel, EmailStr, constr, validator


def validate_email(value: str) -> str:
    if value == None:
        raise ValueError("Email can not be null")
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
        raise ValueError("The email you entered appears to be incorrect.")
    return value

def validate_password(value: str) -> str:
    if value is None:
        raise ValueError("Password cannot be null")
    if len(value) < 5:
        raise ValueError("Password must be at least 5 characters long")
    return value


class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=5)

    @validator('email')
    def validate_register_username(cls, value):
        return validate_email(value)

    @validator('password')
    def validate_register_password(cls, value):
        return validate_password(value)
    
    class Config:
        orm_mode: True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode: True

