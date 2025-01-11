import bcrypt


class PasswordUtils:
    """
    PasswordUtils class to hash and verify passwords
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash the password using bcrypt
        """
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify the password using bcrypt
        """
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
