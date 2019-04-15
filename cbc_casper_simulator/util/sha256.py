import hashlib


class SHA256:
    @classmethod
    def digest(cls, text: str) -> bytes:
        m = hashlib.sha256(text.encode('utf-8'))
        return m.digest()
