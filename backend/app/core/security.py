import hmac
import hashlib
from app.core.settings import settings

def hash_password(password: str):
    return hmac.new(settings.SECRET_KEY.encode("utf-8"), password.encode("utf-8"), hashlib.sha256).hexdigest()


def verify_password(plain_password: str, hashed_password: str):
    pw = hash_password(plain_password)
    return pw == hashed_password


def get_password_hash(password: str):
    return hash_password(password)