from typing import NamedTuple
from collections.abc import Iterator

from application.services.faker import faker


class User(NamedTuple):
    username: str
    email: str

    def get_dict(self) -> dict:
        return self._asdict()

    @classmethod
    def get_fieldnames(cls) -> list[str]:
        return list(cls._fields)

    @classmethod
    def from_raw_dict(cls, raw_data: dict) -> "User":
        return cls(
            username=raw_data["username"],
            email=raw_data["email"],
        )


def generate_user() -> User:
    return User(
        username=faker.first_name(),
        email=faker.email(),
    )


def generate_users(amount: int) -> Iterator[User]:

    for index in range(1, amount + 1):
        yield generate_user()



