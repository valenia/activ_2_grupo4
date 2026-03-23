import hashlib


class HashingPasswordService:

    def __init__(self, algorithm: str = "sha256"):
        self.algorithm = algorithm

    def __call__(self, password: str) -> str:
        return self.hash(password)

    def hash(self, password: str) -> str:
        # Hash password using SHA-256
        return hashlib.sha256(password.encode()).hexdigest()

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        # Verify if a plain password matches a hash
        return self.hash(plain_password) == hashed_password
