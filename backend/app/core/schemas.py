import re
from pydantic import BaseModel, Field, ValidationError, field_validator
from fastapi import Form, HTTPException
from starlette import status


class CryptoFormSchema(BaseModel):
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("must contain at least one uppercase letter")

        if not re.search(r"[a-z]", v):
            raise ValueError("must contain at least one lowercase letter")

        if not re.search(r"[0-9]", v):
            raise ValueError("must contain at least one digit")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>_+-]', v):
            raise ValueError(
                "must contain at least one special character (!@#$%^&* etc.)"
            )

        return v

    @classmethod
    def as_form(cls, password: str = Form(...)):
        try:
            return cls(password=password)
        except ValidationError as e:
            error_details = e.errors()[0]
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Password validation error: {error_details['msg']}",
            )
