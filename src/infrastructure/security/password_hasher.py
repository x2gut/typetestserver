import bcrypt


class PasswordHasher:
    def __init__(self):
        pass

    @staticmethod
    async def hash_password(password: str) -> str:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
        return hashed.decode('utf-8')

    @staticmethod
    async def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
