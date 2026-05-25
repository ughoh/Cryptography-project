import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ValidationError
from fastapi import Form, HTTPException
from starlette import status


class CryptoFormSchema(BaseModel):
    password: str = Field(..., min_length=8)
    second_password: Optional[str] = None

    @field_validator("password", "second_password")
    @classmethod
    def validate_password_strength(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v

        if len(v) < 8:
            raise ValueError("String should have at least 8 characters")

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
    def as_form(
        cls, password: str = Form(...), second_password: Optional[str] = Form(None)
    ):
        try:
            return cls(password=password, second_password=second_password)
        except ValidationError as e:
            error_details = e.errors()[0]
            field_name = error_details["loc"][0]
            display_name = (
                "First password" if field_name == "password" else "Second password"
            )
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"{display_name} validation error: {error_details['msg']}",
            )
