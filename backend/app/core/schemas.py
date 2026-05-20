from fastapi import Form, HTTPException
from pydantic import BaseModel, Field, ValidationError
from starlette import status


class CryptoFormSchema(BaseModel):
    password: str = Field(..., min_length=8)

    @classmethod
    def as_form(cls, password: str = Form(...)):
        try:
            return cls(password=password)

        except ValidationError as e:
            error_details = e.errors()[0]

            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Password validation error: {error_details['msg']}. You entered: '{password}'",
            )
