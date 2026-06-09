import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecureWallet:
    def __init__(self, master_key: str, salt: bytes):
        kdf = PBKDF2HMAC(hashes.SHA256(), 32, salt, 100000)
        self.key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
        self.cipher = Fernet(self.key)

    def encrypt(self, data: str) -> bytes:
        return self.cipher.encrypt(data.encode())
