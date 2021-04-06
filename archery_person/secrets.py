from os import getenv
from cryptography.fernet import Fernet
from argon2 import PasswordHasher
from argon2.exceptions import (
    InvalidHash
)


class Secret:
    """
        Responsible to generate and verify secrets.
    """
    __fernet = Fernet(
        getenv(
            'ARCHERY_PERSON_SECRET'
        )
    )
    __argon = PasswordHasher()

    @property
    def randomic(
        self: object,
        size: int = 36
    ) -> str:
        """
            Generates randomic keys.
        """
        return self.__fernet.generate_key().decode()

    def generate(
        self: object,
        secret: str
    ) -> str:
        """
            Generates password keys from a hash.
        """
        return self.__argon.hash(
            secret
        )

    def verify(
        self: object,
        hash: str,
        secret: str,
    ) -> bool:
        """
            Verify password hash.
        """
        try:
            result = self.__argon.verify(
                hash, secret
            )
        except InvalidHash:
            return False
        return result

    def encrypt(
        self: object,
        message: str
    ) -> str:
        """
            Encrypt messages.
        """
        return self.__fernet.encrypt(
            str(
                message
            ).encode()
        ).decode()

    def decrypt(
        self: object,
        message: str
    ) -> str:
        """
            Decrypt messages.
        """
        value = message if isinstance(
            message,
            bytes
        ) else message.encode()
        return self.__fernet.decrypt(
            value
        ).decode()
