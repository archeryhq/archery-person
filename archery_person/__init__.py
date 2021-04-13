from dotenv import load_dotenv
from archery_auth import Auth
from archery_cookie import Cookie
from archery_secret import Secret


load_dotenv()


class Person:
    """
        Responsible for manage users and cookies.
    """
    __auth = Auth()
    __cookie = Cookie()

    def __set(
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
        """
            Create new person.
        """
        self.__auth.create(
            username=username,
            email=email,
            password=password
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
            self.__set(
                person
            )
            self.cookie = self.__cookie.new(
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
            self.cookie = session
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
