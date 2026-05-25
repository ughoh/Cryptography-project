import io
from urllib.parse import quote

from fastapi import APIRouter, HTTPException, UploadFile, Depends, File
from starlette import status
from starlette.responses import StreamingResponse

from app.core.cryptography import AESEncryptor
from app.core.schemas import CryptoFormSchema

router = APIRouter()


@router.post("/encrypt")
async def encrypt_file(
    file: UploadFile = File(...),
    form_data: CryptoFormSchema = Depends(CryptoFormSchema.as_form),
):
    try:
        file_bytes = await file.read()

        original_filename = file.filename if file.filename else "file"
        if not original_filename.endswith(".enc"):
            encrypted_filename = f"{original_filename}.enc"
        else:
            encrypted_filename = original_filename

        encoded_filename = quote(encrypted_filename)

        passwords = [form_data.password]
        if hasattr(form_data, "second_password") and form_data.second_password:
            passwords.append(form_data.second_password)

        encrypted_data = AESEncryptor.encrypt(file_bytes, passwords)

        return StreamingResponse(
            io.BytesIO(encrypted_data),
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}",
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Encryption error: {str(e)}",
        )
