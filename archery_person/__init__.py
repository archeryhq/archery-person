from dotenv import load_dotenv
load_dotenv()
from archery_person.auths import Auth, create_tables
from archery_person.cookies import Cookie
from archery_person.persons import Person
from archery_person.secrets import Secret


__author__ = "Enio Climaco Sales Junior <eniocsjunior@gmail.com>"
__version__ = "0.1.0"
__all__ = [
    "Auth",
    "Cookie",
    "Person",
    "Secret",
    "create_tables"
]
