import hashlib
import hmac


class HMACX:
    def __init__(self, key: str):
        self.key = key

    def hash(self, data: str) -> str:
        return hmac.new(self.key.encode(), data.encode(), hashlib.sha256).hexdigest()

    def verify(self, data: str, signature: str) -> bool:
        return hmac.compare_digest(self.hash(data), signature)