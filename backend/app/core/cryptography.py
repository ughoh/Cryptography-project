import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


class AESEncryptor:
    @staticmethod
    def _derive_key(password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(password.encode())

    @classmethod
    def encrypt(cls, plaintext: bytes, password: str) -> bytes:
        salt = os.urandom(16)
        nonce = os.urandom(12)

        key = cls._derive_key(password, salt)

        aesgcm = AESGCM(key)

        ciphertext_with_tag = aesgcm.encrypt(nonce, plaintext, associated_data=None)

        ciphertext = ciphertext_with_tag[:-16]
        tag = ciphertext_with_tag[-16:]

        return salt + nonce + tag + ciphertext

    @classmethod
    def decrypt(cls, container: bytes, password: str) -> bytes:
        if len(container) < 44:
            raise ValueError("The file is too short or corrupted.")
        salt = container[0:16]
        nonce = container[16:28]
        tag = container[28:44]
        ciphertext = container[44:]

        key = cls._derive_key(password, salt)

        aesgcm = AESGCM(key)

        ciphertext_with_tag = ciphertext + tag

        plaintext = aesgcm.decrypt(nonce, ciphertext_with_tag, associated_data=None)

        return plaintext
