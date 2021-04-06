from sqlalchemy.exc import IntegrityError
from archery_person.auths import Auth
from archery_person.cookies import (
    Cookie
)
from archery_person.secrets import (
    Secret
)
from archery_person.exceptions import PersonExists


class Person:
    """
        Responsible for manage users and cookies.
    """
    __auth = Auth(
        secret=Secret()
    )
    __cookie = Cookie(
        secret=Secret()
    )

    def __init__(
        self: object,
        cookie: str = None,
        username: str = None,
        password: str = None,
    ) -> None:
        self.renew(
            cookie=cookie
        ) if cookie else None
        self.login(
            username=username,
            password=password
        ) if password else None

    def __set_person(
        self: object,
        data: dict
    ) -> None:
        self.username = data['username']
        self.email = data['email']
        self.enabled = data['enabled']
        self.role = data['role']

    def create(
        self: object,
        username: str,
        email: str,
        password: str
    ) -> bool:
        try:
            self.__auth.add(
                username=username,
                email=email,
                password=password
            )
        except IntegrityError:
            raise PersonExists(
                username=username,
                email=email
            )
        return True

    def login(
        self: object,
        username: str,
        password: str
    ) -> str:
        person = self.__auth.login(
            username,
            password
        )
        if person:
            self.__set_person(person)
            self.cookie = self.__cookie.set(
                person
            )
        return self.cookie

    def renew(
        self: object,
        cookie: str
    ) -> str:
        try:
            session = self.__cookie.renew(
                cookie
            )
        except AttributeError:
            return False
        if session:
            self.__set_person(session)
            self.cookie = session['cookie']
        return self.cookie

    def logout(
        self: object,
        username: str,
        cookie: str
    ) -> bool:
        person = self.__auth.show(
            username
        )
        session = self.__cookie.get(
            cookie
        )
        if self.__secret.decrypt(
            session
        ) == person.id:
            self.__cookie.delete(
                cookie
            )
            return True
        else:
            return False

    def change_password(
        self: object,
        username: str,
        password: str
    ) -> bool:
        self.__auth.change_password(
            username=username,
            password=password
        )
        return True

    def change_email(
        self: object,
        username: str,
        email: str
    ) -> bool:
        self.__auth.change_email(
            username=username,
            email=email
        )
        return True
