import hashlib

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['sha256_crypt'], sha256_crypt__rounds=10_000,deprecated='auto')

def hash_password(password: str) -> str:
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pwd_context.hash(password_hash)

def verify_password(password: str, hashed: str) -> bool:
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pwd_context.verify(password_hash, hashed)