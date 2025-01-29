import re
from typing import Annotated
from pydantic import BaseModel, EmailStr, StringConstraints, field_validator, ConfigDict


class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=5)]

    @field_validator('email')
    def validate_email(cls, value: str) -> str:
        # Check if email is valid or not
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise ValueError("The email you entered appears to be incorrect.")
        return value

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        # Check if the password contains only alphanumeric characters
        if not value.isalnum():
            raise ValueError("Password must contain only alphanumeric characters")
        return value
    
    model_config = ConfigDict(from_attributes=True)


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)

