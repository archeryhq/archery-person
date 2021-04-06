from os import getenv
from json import loads, dumps
from redis import Redis
from archery_person.exceptions import CookieNotFound


class Cookie:
    """
        Responsible for manage cookies.

    """
    __redis = Redis(
        host=getenv(
            'ARCHERY_PERSON_REDIS_HOST'
        ),
        port=getenv(
            'ARCHERY_PERSON_REDIS_PORT'
        ),
        db=getenv(
            'ARCHERY_PERSON_SESSION_DB'
        )
    )

    def __init__(
        self: object,
        secret: callable
    ) -> None:
        self.__secret = secret

    def get(
        self: object,
        cookie: str
    ) -> str:
        try:
            data = loads(
                self.__redis.get(
                    str(cookie)
                ).decode()
            )
        except AttributeError:
            raise CookieNotFound(cookie)
        return data

    def new(
        self: object,
        person: dict
    ) -> str:
        return self.set(
            {
                'id': self.__secret.encrypt(
                    person['id']
                ),
                'username': person['username'],
                'email': person['email'],
                'enabled': person['enabled'],
                'role': person['role']
            }
        )

    def set(
        self: object,
        value: dict
    ) -> str:
        cookie = self.__secret.randomic
        self.__redis.set(
            cookie,
            dumps(value)
        )
        return cookie

    def renew(
        self: object,
        cookie: str
    ) -> str:
        data = self.get(cookie)
        self.__redis.delete(cookie)
        cookie = self.set(data)
        return {
            'cookie': cookie,
            'username': data['username'],
            'email': data['email'],
            'enabled': data['enabled'],
            'role': data['role']
        }
