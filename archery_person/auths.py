from os import getenv
from uuid import uuid4
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    ForeignKey,
    Boolean,
    String,
    DateTime
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql \
    import UUID
from sqlalchemy.orm import sessionmaker
from archery_person.exceptions import LogInError


_engine = create_engine(
    getenv(
        "ARCHERY_PERSON_SQL_URI"
    ),
    echo=True,
    future=True
)
Base = declarative_base()
_Session = sessionmaker(bind=_engine)


class Role(Base):
    """
        Role model.
    """
    __tablename__ = 'roles'
    id = Column(
        UUID(
            as_uuid=True
        ),
        primary_key=True,
        default=uuid4()
    )
    name = Column(
        String(
            length=15
        ),
        nullable=False,
        unique=True
    )
    description = Column(
        String(
            length=50
        ),
        nullable=False
    )


class Person(Base):
    """
        Person model.
    """
    __tablename__ = "persons"
    id = Column(
        UUID(
            as_uuid=True
        ),
        primary_key=True,
        default=uuid4()
    )
    email = Column(
        String(
            length=50
        ),
        nullable=False,
        unique=True
    )
    username = Column(
        String(
            length=25,
        ),
        nullable=False,
        unique=True
    )
    password = Column(
        String(
            length=125,
            convert_unicode=True
        ),
        nullable=False
    )
    role = Column(
        UUID(
            as_uuid=True
        ),
        ForeignKey('roles.id')
    )
    create_in = Column(
        DateTime(),
        default=datetime.now()
    )
    enabled = Column(
        Boolean(),
        default=False
    )


def create_tables():
    """
        Initialize database.
    """
    Base.metadata.drop_all(_engine)
    Base.metadata.create_all(_engine)


class Auth:
    """
        Responsible for communicating with the database, managing users.

    """

    def __init__(
        self: object,
        secret: callable
    ) -> None:
        self.__secret = secret
        self.__session = _Session()

    def add(
        self: object,
        username: str,
        email: str,
        password: str
    ) -> None:
        self.__session.add(
            Person(
                username=username,
                email=email,
                password=self.__secret.generate(
                    password
                )
            )
        )
        self.__session.commit()

    def login(
        self: object,
        username: str,
        password: str
    ) -> str:
        person = self.__show(
            username
        )
        if self.__secret.verify(
            person.password,
            password
        ) is True:
            self.id = self.__secret.encrypt(person.id)
            self.username = person.username
            self.email = person.email
            self.role = person.role
            self.enabled = person.enabled
            return {
                'id': self.id,
                'username': self.username,
                'email': self.email,
                'role': self.role,
                'enabled': self.enabled
            }
        else:
            raise LogInError(username)

    def __show(
        self: object,
        username: str
    ) -> dict:
        person = self.__session.query(
            Person
        ).filter_by(
            username=username
        ).first()
        return person

    def change_password(
        self: object,
        username: str,
        password: str
    ) -> bool:
        person = self.__session.query(
            Person
        ).filter_by(
            username=username
        ).first()
        person.password = self.__secret.generate(
            password
        )
        self.__session.commit()
        return True

    def change_email(
        self: object,
        username: str,
        email: str
    ) -> bool:
        person = self.__session.query(
            Person
        ).filter_by(
            username=username
        ).first()
        person.email = email if person.id == self.id else False
        self.__session.commit()
        return True
