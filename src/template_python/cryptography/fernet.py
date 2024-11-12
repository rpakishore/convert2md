import secrets
from base64 import urlsafe_b64encode
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from ..utils.logger import log

__TIMETOKEN: int = 156623378

def __derive_key(password: str) -> bytes:
    """Derive a key from a password using PBKDF2-HMAC-SHA256"""
    password_bytes = password.encode()
    _package = Path(__file__).parent.parent / "Session.key"
    if _package.is_file():
        with open(_package, "rb") as f:
            salt = f.read()
    else:
        salt = secrets.token_bytes(32)
        with open(_package, "wb") as f:
            f.write(salt)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), iterations=100000, salt=salt, length=32)
    key = urlsafe_b64encode(kdf.derive(password_bytes))
    return key

def encrypt_text(text: str, password: str) -> str:
    """Encrypt a text using a password and the Fernet algorithm"""
    key = __derive_key(password)
    cipher_suite = Fernet(key, __TIMETOKEN)
    encrypted_text = cipher_suite.encrypt(text.encode())
    return encrypted_text.decode()


def decrypt_text(encrypted_text: str | bytes, password: str) -> str:
    """Decrypt an encrypted text using a password and the Fernet algorithm"""
    try:
        if isinstance(encrypted_text, str):
            encrypted_text = encrypted_text.encode()
        key = __derive_key(password)
        cipher_suite = Fernet(key, __TIMETOKEN)
        decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
        return decrypted_text
    except InvalidToken:
        log.error("Decryption failed. Invalid token or incorrect password.")
        return ""
