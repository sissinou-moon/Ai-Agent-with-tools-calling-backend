# pyrefly: ignore [missing-import]
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

class PasswordService:
    @staticmethod
    def hash(password: str) -> str:
        return password_hash.hash(password)

    @staticmethod
    def verify(password: str, hashed: str) -> bool:
        return password_hash.verify(password, hashed)