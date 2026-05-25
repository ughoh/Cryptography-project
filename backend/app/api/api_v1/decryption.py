import io
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from starlette import status
from starlette.responses import StreamingResponse

from app.core.cryptography import AESEncryptor
from app.core.schemas import CryptoFormSchema

router = APIRouter()


@router.post("/decrypt")
async def decrypt_file(
    file: UploadFile = File(...),
    form_data: CryptoFormSchema = Depends(CryptoFormSchema.as_form),
):
    try:
        encrypted_bytes = await file.read()

        filename = file.filename if file.filename else "decoded_file"
        if filename.endswith(".enc"):
            original_filename = filename[:-4]
        else:
            original_filename = filename if filename else "decoded_file"

        encoded_filename = quote(original_filename)

        passwords = [form_data.password]
        if hasattr(form_data, "second_password") and form_data.second_password:
            passwords.append(form_data.second_password)

        decrypted_data = AESEncryptor.decrypt(encrypted_bytes, passwords)

        return StreamingResponse(
            io.BytesIO(decrypted_data),
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}",
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The password is incorrect or the file is corrupted (integrity is compromised).",
        )
