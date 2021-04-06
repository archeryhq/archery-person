class CookieNotFound(Exception):
    def __init__(
        self: object,
        cookie: str
    ) -> None:
        self.cookie = cookie

    def __str__(self) -> str:
        return f'Cookie { self.cookie } not found!'


class PersonExists(Exception):
    def __init__(
        self: object,
        username: str,
        email: str
    ) -> None:
        self.username = username
        self.email = email

    def __str__(self) -> str:
        return 'Person ' +\
            self.username +\
            ' or email ' +\
            self.email +\
            ' exists!'


class LogInError(Exception):
    def __init__(
        self: object,
        username: str
    ) -> None:
        self.username = username

    def __str__(self) -> str:
        return f'Error in authorization of person ' +\
            self.username + '!'
