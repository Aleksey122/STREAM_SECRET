import hashlib
import base64
from cryptography.fernet import Fernet

class SecureWallet:
    def __init__(self, master_key):
        self.key = hashlib.sha256(master_key.encode()).hexdigest()[:32].encode()
        self.cipher = Fernet(base64.urlsafe_b64encode(self.key))
        self.vault = {}
        self.is_locked = False

    def trigger_panic(self):
        self.vault.clear()
        self.is_locked = True
        print("[!] ALERT: Система переведена в режим полной защиты.")

    def add_asset(self, asset_id, data):
        if not self.is_locked:
            encrypted_data = self.cipher.encrypt(data.encode())
            self.vault[asset_id] = encrypted_data
            print(f"[+] Активы {asset_id} зашифрованы.")

    def get_status(self):
        return "SECURE" if not self.is_locked else "LOCKED"

if __name__ == "__main__":
    wallet = SecureWallet("my_super_secret_master_key")
    wallet.add_asset("ruble_digital", "balance: 100000")
    print(f"Статус: {wallet.get_status()}")
