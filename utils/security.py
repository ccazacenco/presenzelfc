"""
Crittografia dati sensibili con Fernet.
"""

from cryptography.fernet import Fernet
import os
from config.settings import SECRET_KEY_PATH

def _get_key() -> bytes:
    if not os.path.exists(SECRET_KEY_PATH):
        key = Fernet.generate_key()
        with open(SECRET_KEY_PATH, 'wb') as f:
            f.write(key)
    else:
        with open(SECRET_KEY_PATH, 'rb') as f:
            key = f.read()
    return key

fernet = Fernet(_get_key())

def encrypt(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()