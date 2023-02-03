import bcrypt


class Passwords:
    @staticmethod
    def hash_password(password: str):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password

    @staticmethod
    def verify_password(password: str, hashed_password: str):
        return bcrypt.checkpw(password.encode(), hashed_password)
